import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import DatabaseError, transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from ehms.activities.views import create_activity
from ehms.patients.models import Patient, PatientImage

from .forms import FamilyRelationForm
from .models import FamilyTree
from ehms.core.decorators import logged_in_user, fetch_user_details, check_token


@login_required
@logged_in_user(['hospital level', 'practitioner level'])
@fetch_user_details
@check_token(['practitioner level'])
def relation_fetch(request, pk):
    """
    Fetch the stored relations of the patient

    :param request: HttpRequest Object
    :param pk: Primary key of the patient
    :return: relations of the patient
    """
    patient = get_object_or_404(Patient, status='active', pk=pk)

    # record
    create_activity(request, 'GET', _('Family data is fetched for the patient.'), 'Hospital', patient)

    relations = FamilyTree.objects.filter(
        first_patient=patient
    ).select_related(
        'first_patient',
        'second_patient'
    )

    patient_image = PatientImage.objects.filter(
        status='active',
        current_image=True,
    )

    context = {
        'title': 'Relation | Patient',
        'patient': patient,
        'patient_image': patient_image,
        'relations': relations
    }

    return render(request, 'family_tree/relation_fetch.html', context)


@login_required
@logged_in_user(['hospital level', 'practitioner level'])
@fetch_user_details
@check_token(['practitioner level'])
def patient_relation(request):
    """
    Create a patient relation
    To do so we require UIDs of two patients
    who's relation you want to create

    :param request: HttpRequest Object
    :return: Confirmation whether the relation is created or not
    """
    if request.method == 'POST':
        first_patient = None
        second_patient = None
        flag = False
        form = FamilyRelationForm(request.POST or None)
        if form.is_valid():
            # check if both the UID submitted by user are not the same
            # both the UIDs should be different to form a relation
            if request.POST['first_patient'] != request.POST['second_patient']:
                # check if both the UIDs exists or valid
                try:
                    # check if UIDs submitted are valid or not
                    first_patient = Patient.objects.get(status='active', uid=form.cleaned_data.get('first_patient'))
                    second_patient = Patient.objects.get(status='active', uid=form.cleaned_data.get('second_patient'))
                except Patient.DoesNotExist:
                    flag = True
                    # record
                    create_activity(
                        request,
                        'INSERT ERROR',
                        _('Patient relation is tried to create with UIDs %(uid1)s - %(uid2)s') % {
                            'uid1': form.cleaned_data.get('first_patient'),
                            'uid2': form.cleaned_data.get('second_patient')
                        }, 'Hospital'
                    )
                if flag:
                    messages.error(request, 'Please check both the UIDs. Make sure they are correct.')
                elif FamilyTree.objects.filter(first_patient=first_patient.pk, second_patient=second_patient.pk).exists():
                    messages.error(request, 'First Person to second person relation already exist.')
                elif FamilyTree.objects.filter(first_patient=second_patient.pk, second_patient=first_patient.pk).exists():
                    messages.error(request, 'Second Person to first person relation already exist.')
                else:
                    flag2 = True

                    try:
                        with transaction.atomic():
                            FamilyTree(
                                first_patient=first_patient,
                                second_patient=second_patient,
                                relation=form.cleaned_data.get('first_to_second_relation'),
                                creator_user=request.user,
                                hospital=request.hospital,
                            ).save()
                            FamilyTree(
                                first_patient=second_patient,
                                second_patient=first_patient,
                                relation=form.cleaned_data.get('second_to_first_relation'),
                                creator_user=request.user,
                                hospital=request.hospital,
                            ).save()

                            create_activity(
                                request,
                                'INSERT',
                                _('Patient relation is created with UIDs %(uid1)s - %(uid2)s') % {
                                    'uid1': first_patient,
                                    'uid2': second_patient,
                                }, 'Hospital'
                            )

                    except DatabaseError:
                        flag2 = False
                        transaction.set_rollback(True)

                    if flag2:
                        messages.success(request, 'Relation is created.')
                        return redirect('family_tree:relation')
                    else:
                        messages.error(request, 'Something went wrong. Try again.')
            else:
                messages.error(request, 'Same person relation can not be created.')
    else:
        form = FamilyRelationForm()

    context = {
        'title': 'Create Relation | Patient',
        'form': form
    }

    return render(request, 'family_tree/relation.html', context)
