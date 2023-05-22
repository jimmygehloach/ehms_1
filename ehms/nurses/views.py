import re
import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.db import transaction, IntegrityError, DatabaseError
from django.http import Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render

from django.utils.dateparse import parse_datetime
from django.utils.translation import gettext_lazy as _

from ehms.core.decorators import logged_in_user, fetch_user_details, check_token
from ehms.nurses.models import Nurse, NurseHospital, VitalSignRecord, NurseNotes, IntakeOutputChart
from ehms.activities.views import create_activity
from ehms.medical_sessions.models import MedicalSession

from . import forms
from .forms import NewVitalSignRecordForm, NewIntakeOutputChartForm
from ..core.utils import check_activity_level, verhoeff_random_number, is_valid_uuid, kurrent_timestamp


@login_required
@logged_in_user(['hospital level'])
@fetch_user_details
def nurses_in_hospital_list(request):
    """
    Nurse list in the hospital

    :param request: HTTP request object
    :return: list of nurses in the hospital
    """
    is_paginated = False
    nurses = None

    create_activity(request, 'GET', _('Nurses list is fetched.'), 'Hospital')

    count = NurseHospital.objects.filter(
        hospital_id=request.hospital.pk,
        status='active',
        current_hospital=True,
        nurse__status='active'
    ).select_related('nurse').count()

    sort_by = request.GET.get('sort')
    if sort_by not in ['asc', 'desc']:
        sort_by = 'desc'

    if sort_by == 'asc':
        nurses = NurseHospital.objects.filter(
            hospital_id=request.hospital.pk,
            status='active',
            current_hospital=True,
            nurse__status='active'
        ).select_related('nurse').order_by('created')

    elif sort_by == 'desc':
        nurses = NurseHospital.objects.filter(
            hospital_id=request.hospital.pk,
            status='active',
            current_hospital=True,
            nurse__status='active'
        ).select_related('nurse').order_by('-created')

    paginator = Paginator(nurses, 30)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if count > 30:
        is_paginated = True

    context = {
        'title': 'List | Nurses',
        'is_paginated': is_paginated,
        'page_obj': page_obj,
        'nurse_count': count
    }

    return render(request, 'nurses/nurse_in_hospital_list.html', context)


@login_required
@logged_in_user(['hospital level', 'nurse level', 'practitioner level'])
@fetch_user_details
def nurse_profile_page(request, pk):
    """
    Get a nurse profile

    :param request:HTTP request object
    :param pk: primary key of the nurse
    :return: nurse detail or 404
    """
    nurse = get_object_or_404(Nurse, pk=pk, status='active')

    create_activity(request, 'GET', _('Nurse profile is visited.'), check_activity_level(request))

    nurse_hospitals = NurseHospital.objects.filter(nurse_id=nurse.pk, nurse__status='active', status='active', )

    data_send = {
        'title': 'Profile | Nurse',
        'nurse': nurse,
        'nurse_hospitals': nurse_hospitals,
    }

    return render(request, 'nurses/nurse_detail.html', data_send)


@login_required
@logged_in_user(['nurse level'])
@fetch_user_details
def nurse_dashboard(request):
    """
    Nurse Dashboard

    :param request:HTTP request object
    :return: Dashboard elements / data
    """
    instance = get_object_or_404(Nurse, pk=request.nurse.pk, status='active') #TODO also check the hospital or check it somewhere else
    nurse_name = request.nurse.first_name + ' ' + request.nurse.last_name

    create_activity(
        request,
        'GET',
        _('Nurse Dashboard is visited. Name: - %(name)s.') % {'name': nurse_name, },
        check_activity_level(request)
    )

    vital_sign_record = VitalSignRecord.objects.filter(nurse=request.nurse, status='active', ).count()
    intake_output_chart = IntakeOutputChart.objects.filter(nurse=request.nurse, status='active', ).count()
    nurse_notes = NurseNotes.objects.filter(nurse=request.nurse, status='active', ).count()

    data_send = {
        'nurse': instance,
        'title': 'Dashboard',
        'total_vsr': vital_sign_record,
        'total_ioc': intake_output_chart,
        'total_notes': nurse_notes,
    }
    return render(request, 'nurses/dashboard.html', data_send)


@login_required
@logged_in_user(['hospital level'])
@fetch_user_details
def nurse_token_request_page(request):
    """

    :param request:
    :return:
    """
    nurses = []
    is_paginated = False
    nurses = None

    create_activity(request, 'GET', _('Nurse token page is visited.'), check_activity_level(request))

    nurses = NurseHospital.objects.filter(
        hospital=request.hospital,
        status='active',
        current_hospital=True,
        nurse__status='active'
    ).select_related('nurse')

    sort_by = request.GET.get('sort')

    if sort_by not in ['asc', 'desc']:
        sort_by = 'desc'

    if sort_by == 'asc':
        nurses = nurses.order_by('created')
    elif sort_by == 'desc':
        nurses = nurses.order_by('-created')

    paginator = Paginator(nurses, 30)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if paginator.count > 30:
        is_paginated = True

    if request.method == 'POST':
        if 'token_timestamp' in request.POST and 'nurse' in request.POST:
            nurse_data = request.POST['nurse']
            timestamp_data = request.POST['token_timestamp']

            if timestamp_data != '' and nurse_data != '':
                timestamp_pattern = re.compile(r'^(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2})$')
                if timestamp_pattern.match(timestamp_data):
                    if parse_datetime(timestamp_data).timestamp() > kurrent_timestamp():
                        try:
                            nurse = Nurse.objects.filter(pk=nurse_data, status='active').first()
                        except Nurse.DoesNotExist:
                            nurse = None
                        if nurse:
                            try:
                                with transaction.atomic():
                                    nurse.token = verhoeff_random_number(1, 8)
                                    nurse.token_timestamp = request.POST.get('token_timestamp')
                                    nurse.verify_token = False
                                    nurse.save()
                                    messages.success(request, _('Token generated.'))

                                    nurse_name = nurse.first_name + ' ' + nurse.last_name
                                    message = \
                                    _('Nurse token is generated. Name: - %(name)s.') % {'name': nurse_name, }
                                    create_activity(request, 'UPDATE', message, check_activity_level(request))
                                    return redirect(reverse('nurses:token'))
                            except DatabaseError:
                                messages.error(request, _('Something went wrong.'))
                        else:
                            messages.error(request, _('Invalid nurse id. Try again.'))
                    else:
                        messages.error(request, _('You cannot assign previous date time. Try again.'))
                else:
                    messages.error(request, _('Invalid date time of token. Try again.'))
            else:
                messages.error(request, _('Invalid data send. Check both the fields and try again.'))
        else:
            messages.error(request, _('Something went wrong. Try again.'))

    data_send = {
        'title': 'Token | Nurse',
        'page_obj': page_obj,
        'nurses_count': paginator.count,
        'is_paginated': is_paginated,
    }

    return render(request, 'nurses/login_token.html', data_send)


@login_required
@logged_in_user(['nurse level'])
@fetch_user_details
@check_token(['nurse level'])
def nurse_vital_sign_record(request, pk):
    """
    Record the vital signs of patient when its medical session record exists.
    Vital sign record depends on medical session of the patient.

    :param request: HTTP request object
    :param pk: Medical session primary key
    :return: Creates a VSR or returns an error
    """

    medical_session = get_object_or_404(MedicalSession, pk=pk, status="active", hospital=request.hospital)

    # Patient
    p = medical_session.patient

    create_activity(
        request,
        'GET',
        _('Nurse vital sign record form page visited by: - %(nurse)s') % {'nurse': request.nurse},
        check_activity_level(request),
        p
    )

    if request.method == 'POST':
        form = NewVitalSignRecordForm(request.POST or None)
        if form.is_valid():
            try:
                with transaction.atomic():
                    vsr = form.save(commit=False)
                    vsr.creator_user = request.user
                    vsr.medical_session = medical_session
                    vsr.nurse = request.nurse
                    vsr.hospital = request.hospital
                    vsr.patient = p
                    vsr.save()

                    create_activity(
                        request,
                        'INSERT',
                        _('Nurse vital sign record created by: - %(nurse)s') % {'nurse': request.nurse},
                        check_activity_level(request),
                        p
                    )

                messages.success(request, _('Vital sign record created.'))
                return redirect(
                    reverse('medical_sessions:detail', args=(p.pk, medical_session.uid,))
                )
            except DatabaseError:
                messages.error(request, _('Something went wrong.'))
    else:
        form = NewVitalSignRecordForm()

    data_send = {
        'title': 'VSR Form | Nurse',
        'form': form,
        'patient': p,
    }

    return render(request, 'nurses/vital_sign_records.html', data_send)


@login_required
@logged_in_user(['nurse level'])
@fetch_user_details
@check_token(['nurse level'])
def nurse_vital_sign_record_detail(request, pk):
    vsr = VitalSignRecord.objects.filter(
        pk=pk,
        hospital=request.hospital,
        status='active'
    ).select_related(
        'nurse',
        'patient',
    ).order_by('-created').first()

    if vsr is None:
        raise Http404

    create_activity(
        request,
        'GET',
        _('Nurse vital sign record detail page visited'),
        check_activity_level(request),
        vsr.patient
    )

    data_send = {
        'title': 'VSR Detail | Nurse',
        'vsr': vsr,
    }

    return render(request, 'nurses/vital_sign_records_detail.html', data_send)


@login_required
@logged_in_user(['nurse level'])
@fetch_user_details
@check_token(['nurse level'])
def nurse_intake_output_chart(request, pk):
    """
    Record the intake output details os in-patients.
    Intake output chart depends on medical session of the patient.

    :param request: HTTP request object
    :param pk: Medical session primary key
    :return: Creates an IOC or returns an error
    """
    medical_session = get_object_or_404(MedicalSession, pk=pk, status="active", hospital=request.hospital)
    p = medical_session.patient

    create_activity(
        request,
        'GET',
        _('Nurse intake output chart form page visited by: - %(nurse)s') % {'nurse': request.nurse},
        check_activity_level(request),
        p
    )

    if request.method == 'POST':
        form = NewIntakeOutputChartForm(request.POST or None)
        if form.is_valid():
            try:
                with transaction.atomic():
                    vsr = form.save(commit=False)
                    vsr.creator_user = request.user
                    vsr.medical_session = medical_session
                    vsr.nurse = request.nurse
                    vsr.hospital = request.hospital
                    vsr.patient = p
                    vsr.save()

                    create_activity(
                        request,
                        'INSERT',
                        _('Nurse input output chart created by: - %(nurse)s') % {'nurse': request.nurse},
                        check_activity_level(request),
                        p
                    )

                messages.success(request, _('Intake output chart created.'))

                return redirect(
                    reverse(
                        'medical_sessions:detail',
                        args=(p.pk, medical_session.uid,)
                    )
                )

            except DatabaseError:
                print(traceback.format_exc())
                messages.error(request, _('Something went wrong.'))
    else:
        form = NewIntakeOutputChartForm()

    data_send = {
        'title': 'IOC Form | Nurse',
        'form': form,
        'patient': p
    }

    return render(request, 'nurses/intake_output_charts.html', data_send)


@login_required
@logged_in_user(['nurse level'])
@fetch_user_details
@check_token(['nurse level'])
def nurse_intake_output_chart_detail(request, pk):
    ioc = IntakeOutputChart.objects.filter(
        pk=pk,
        hospital=request.hospital,
        status='active'
    ).select_related(
        'nurse',
        'patient',
    ).order_by('-created').first()

    if ioc is None:
        raise Http404

    create_activity(
        request,
        'GET',
        _('Nurse vital sign record detail page visited'),
        check_activity_level(request),
        ioc.patient
    )

    data_send = {
        'title': 'VSR Detail | Nurse',
        'ioc': ioc,
    }

    return render(request, 'nurses/intake_output_chart_detail.html', data_send)


@login_required
@logged_in_user(['nurse level'])
@fetch_user_details
@check_token(['nurse level'])
def nurses_notes(request, pk):
    """
    Record the notes of the in-patients.
    Nurse notes depends on medical session of the patient.

    :param request: HTTP request object
    :param pk: Medical session primary key
    :return: Creates a note or returns an error
    """
    medical_session = get_object_or_404(MedicalSession, pk=pk, status="active")
    p = medical_session.patient

    create_activity(
        request,
        'GET',
        _('Nurse notes form page visited by: - %(nurse)s') % {'nurse': request.nurse},
        check_activity_level(request),
        p
    )
    if request.method == 'POST':
        form = forms.NewNurseNotesForm(request.POST or None)
        if form.is_valid():
            try:
                with transaction.atomic():
                    vsr = form.save(commit=False)
                    vsr.creator_user = request.user
                    vsr.medical_session = medical_session
                    vsr.nurse = request.nurse
                    vsr.hospital = request.hospital
                    vsr.patient = p
                    vsr.save()
                    messages.success(request, _('Notes created.'))

                    create_activity(
                        request,
                        'GET',
                        _('Nurse vital sign record detail page visited by: - %(nurse)s') % {'nurse': request.nurse},
                        check_activity_level(request)
                    )

                    return redirect(
                        reverse(
                            'medical_sessions:detail',
                            args=(p.pk, medical_session.uid,)
                        )
                    )

            except IntegrityError:
                messages.error(request, _('Something went wrong.'))
    else:
        form = forms.NewNurseNotesForm()

    data_send = {
        'title': 'Notes Form | Nurse',
        'form': form,
        'patient': p
    }

    return render(request, 'nurses/nurse_notes.html', data_send)


@login_required
@logged_in_user(['nurse level'])
@fetch_user_details
@check_token(['nurse level'])
def nurse_notes_detail(request, pk):
    nn = NurseNotes.objects.filter(
        pk=pk,
        hospital=request.hospital,
        status='active'
    ).select_related(
        'nurse',
        'patient',
    ).order_by('-created').first()

    if nn is None:
        raise Http404

    create_activity(
        request,
        'GET',
        _('Nurse note record detail page visited'),
        check_activity_level(request),
        nn.patient
    )

    data_send = {
        'title': 'Note Detail | Nurse',
        'nn': nn
    }
    return render(request, 'nurses/nurse_notes_detail.html', data_send)
