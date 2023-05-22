from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction, DatabaseError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ehms.activities.views import create_activity
from ehms.core.decorators import logged_in_user, fetch_user_details
from ehms.core.utils import check_activity_level
from ehms.mortuaries.forms import NewMortuaryPatientForm, ReleaseMortuaryPatientForm
from ehms.mortuaries.models import Mortuary, MortuaryPatient
from ehms.patients.models import Patient, PatientDeathRecord


@login_required
@logged_in_user(['hospital level', 'mortuary level'])
@fetch_user_details
def add_patient_to_mortuary(request, pk):
    """
    Add an existing patient record to mortuary, if the patient is declared dead.

    :param request: HTTP request Object
    :param pt: primary key of the patient
    :return: returns a response back to patient detail page.
            Response 1. You cannot add patient to mortuary
            Response 2. You can add patient to mortuary
    """

    patient = None

    try:
        # fetch the record of the patient to figure out it belongs to the same hospital
        patient = Patient.objects.get(pk=pk, hospital=request.hospital, status='active')
    except Patient.DoesNotExist:
        messages.info(request, _('Patient does not belong to this hospital.'))
        return redirect(reverse('patients:detail', args=(pk,)))

    # check vital status of patient
    if not patient.vital_status:
        # record = PatientDeathRecord.objects.filter(patient=patient, status='active').first()
        # # check the death record of patient
        # if not record:
        #     messages.error(request, _('The patient death record not found.'))
        #     return redirect(reverse('patients:detail', args=(pk,)))
        # else:
        mortuary_check = MortuaryPatient.objects.filter(patient=patient, status='active')
        # check if patient is already in mortuary
        if mortuary_check:
            messages.error(request, _('Patient is already in mortuary.'))
            return redirect(reverse('patients:detail', args=(pk,)))
    else:
        messages.error(request, _('The patient is still alive or not updated as dead.'))
        return redirect(reverse('patients:detail', args=(pk,)))

    create_activity(request, 'GET', _('Add patient to mortuary page is visited.'), check_activity_level(request), patient)

    if request.method == 'POST':
        form = NewMortuaryPatientForm(request.POST or None)

        if form.is_valid():
            try:
                with transaction.atomic():
                    __mortuary = form.save(commit=False)
                    __mortuary.patient = patient
                    __mortuary.in_mortuary = True
                    __mortuary.hospital = request.hospital
                    __mortuary.creator_user = request.user
                    __mortuary.save()

                    create_activity(
                        request,
                        'INSERT',
                        _('Patient is added to mortuary.'),
                        check_activity_level(request),
                        patient
                    )

                messages.success(request, _('Record is added to mortuary.'))
                return redirect(reverse('mortuaries:home', args=(pk,)))
            except DatabaseError:
                messages.error(request, _('Something went wrong. Try again.'))
                return redirect(reverse('patients:detail', args=(pk,)))
    else:
        form = NewMortuaryPatientForm()

    data_send = {
        'title': 'Add | Mortuary',
        'patient': patient,
        'form': form,
    }

    return render(request, "mortuaries/add-new-patient.html", data_send)\


@login_required
@logged_in_user(['hospital level', 'mortuary level'])
@fetch_user_details
def patient_release_from_mortuary(request, pk, pt):

    try:
        mortuary = Mortuary.objects.get(pk=pk, hospital=request.hospital, status='active')
        patient = Patient.objects.get(pk=pt, hospital=request.hospital, vital_status=False, status='active')
    except (Mortuary.DoesNotExist, Patient.DoesNotExist) as e:
        messages.error(request, _('Something went wrong. Please check your records.'))
        return redirect(reverse('mortuaries:list', args=(pk,)))

    create_activity(
        request,
        'GET',
        _('Release patient body from mortuary form is visited.'),
        check_activity_level(request),
        patient
    )

    mortuary_check = MortuaryPatient.objects.filter(patient=patient, status='active', in_mortuary=True)
    # check if patient is already in mortuary
    if not mortuary_check:
        messages.error(request, _('Patient is not in mortuary.'))
        return redirect(reverse('patients:list', args=(pk,)))

    if request.method == 'POST':
        form = ReleaseMortuaryPatientForm(request.POST or None)

        if form.is_valid():
            try:
                with transaction.atomic():
                    __mortuary = form.save(commit=False)
                    __mortuary.patient = patient
                    __mortuary.in_mortuary = False
                    __mortuary.hospital = request.hospital
                    __mortuary.creator_user = request.user
                    __mortuary.save()

                    create_activity(
                        request,
                        'UPDATE',
                        _('Patient body is released from mortuary.'),
                        check_activity_level(request),
                        patient
                    )

                messages.success(request, _('Patient body is released from mortuary.'))
                return redirect(reverse('mortuaries:list', args=(pk,)))
            except DatabaseError:
                messages.error(request, _('Something went wrong. Try again.'))
                return redirect(reverse('patients:list', args=(pk,)))
    else:
        form = ReleaseMortuaryPatientForm()

    data_send = {
        'title': 'Release | Mortuary',
        'patient': patient,
        'mortuary': mortuary,
        'form': form,
    }

    return render(request, "mortuaries/release-patient-from-mortuary.html", data_send)


@login_required
@logged_in_user(['hospital level', 'mortuary level'])
@fetch_user_details
def patients_in_mortuary(request, pk):
    """
    Get a record of patients entered in mortuary after their death.

    :param request: HTTP request object
    :param pk: primary key of mortuary in the hospital
    :return: record of patients entered in mortuary after their death.
    """
    mortuary = get_object_or_404(Mortuary, hospital=request.hospital, pk=pk, status='active')

    create_activity(request, 'GET', _('List of patients in mortuary page is visited. Mortuary: - %(m)s') % {'m': mortuary.name}, check_activity_level(request))

    patients = MortuaryPatient.objects.filter(
        mortuary=mortuary,
        status='active',
    ).select_related('patient', 'mortuary')

    data_send = {
        'title': 'List | Mortuary',
        'patients': patients,
    }

    return render(request, "mortuaries/patients-in-mortuary.html", data_send)


@login_required
@logged_in_user(['hospital level', 'mortuary level'])
@fetch_user_details
def patients_detail_in_mortuary(request, pk, pt):
    """
    Get the Patient detail from the mortuary

    :param request: HTTP request object
    :param pk: primary key of the mortuary
    :param pt: primary key of the patient
    :return: patient detail in the mortuary or None
    """
    mortuary = get_object_or_404(Mortuary, hospital=request.hospital, pk=pk, status='active')

    patient = get_object_or_404(Patient, hospital=request.hospital, pk=pt, status='active')

    create_activity(
        request,
        'GET',
        _('Patient detail in mortuary page is visited. Mortuary: - %(m)s') % {'m': mortuary.name},
        check_activity_level(request)
    )

    patient_detail = MortuaryPatient.objects.filter(
        mortuary=mortuary,
        status='active',
        patient=patient
    ).select_related('patient', 'mortuary', 'hospital').first()

    context = {
        'title': 'Patient Detail | Mortuary',
        'mortuary': mortuary,
        'patient': patient,
        'detail': patient_detail,
    }

    return render(request, "mortuaries/mortuary-in-patient-detail.html", context)


@login_required
@logged_in_user(['hospital level', 'mortuary level'])
@fetch_user_details
def mortuaries_list(request):
    """
    Get the mortuary list within an hospital

    :param request: HTTP request object
    :return: list of mortuaries
    """
    mortuaries = Mortuary.objects.filter(hospital=request.hospital, status='active')

    create_activity(
        request, 'GET',
        _('Mortuary list page is visited'),
        check_activity_level(request)
    )

    context = {
        'title': 'Mortuaries',
        'mortuaries': mortuaries,
    }

    return render(request, "mortuaries/main.html", context)


@login_required
@logged_in_user(['hospital level', 'mortuary level'])
@fetch_user_details
def mortuary_detail(request, pk):
    """
    Get the individual mortuary detail

    :param request: HTTP request object
    :param pk: primary key of the mortuary detail
    :return: detail of mortuary or 404
    """
    mortuary = get_object_or_404(Mortuary, hospital=request.hospital, status='active', pk=pk)
    create_activity(request, 'GET', _('Mortuary detail page is visited. Mortuary: - %(m)s') % {'m': mortuary.name}, check_activity_level(request))
    context = {
        'title': 'Detail | Mortuary',
        'mortuary': mortuary,
    }

    return render(request, "mortuaries/mortuary-detail.html", context)
