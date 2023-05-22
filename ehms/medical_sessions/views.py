from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction, DatabaseError
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ehms.activities.views import create_activity

from . import forms
from ehms.patients.models import Patient

from .models import MedicalSession, Department
from ehms.core.decorators import logged_in_user, fetch_user_details, check_token
from ..nurses.models import VitalSignRecord, IntakeOutputChart, NurseNotes  # TODO: look into this


def check_activity_tag(request):
    activity_tag = 'Practitioner'
    if request.group_name == 'hospital level':
        activity_tag = 'Hospital'
    elif request.group_name == 'nurse level':
        activity_tag = 'Nurse'

    return activity_tag


@login_required
@logged_in_user(['practitioner level'])
@fetch_user_details
@check_token(['practitioner level'])
def medical_session_create(request, pk):
    patient = get_object_or_404(Patient, pk=pk, status='active', hospital_id=request.hospital.pk)
    create_activity(request, 'GET', _('Medical session create page is visited'), 'Practitioner', patient)
    department = get_object_or_404(Department, name='IPD', status='active')
    beds_occupied = MedicalSession.objects.filter(status='active', hospital=request.hospital, department=department,
                                                  ipd_status='Occupied', ).count()
    beds_available = request.hospital.beds - beds_occupied
    if request.method == 'POST':
        medical_session_form = forms.NewMedicalSessionForm(request.POST or None, request.FILES or None)
        if medical_session_form.is_valid():
            ms_record = None
            if medical_session_form.cleaned_data['department'] == 'IPD':
                # TODO: check if that patient has previously occupied session
                # ms= medical session
                ms_record = MedicalSession.objects.filter(status='active', hospital=request.hospital,
                                                          department=department, ipd_status='Occupied',
                                                          patient=Patient).first()
            try:
                with transaction.atomic():
                    # Update previous medical session of the patient if occupied
                    if ms_record:
                        ms_record.ipd_status = 'Not Applicable'

                    medical_session = medical_session_form.save(commit=False)
                    medical_session.hospital = request.hospital
                    medical_session.patient = patient
                    medical_session.practitioner = request.practitioner
                    medical_session.creator_user = request.user
                    medical_session.save()
                    medical_session.creation_place = "Practitioner"
                    medical_session_form.save_m2m()

                messages.success(request, _('New medical session created.'))
                create_activity(request, 'INSERT', _('Patient Medical Sessions is created'), 'Practitioner', patient)
                return redirect(reverse('medical_sessions:new', args=(pk,)))
            except DatabaseError:
                messages.error(request, _('Something went wrong.'))
        else:
            messages.error(request, _('Something went wrong. Check the errors.'))
    else:
        medical_session_form = forms.NewMedicalSessionForm()

    context = {
        'title': 'New Medical Session',
        'hospital_user': True,
        'medical_session_form': medical_session_form,
        'hospital_name': request.hospital.name,
        'patient': patient,
        'beds_available': beds_available,
    }

    return render(request, "medical_sessions/medical_session_create.html", context)


@login_required
@logged_in_user(['hospital level', 'practitioner level', 'nurse level'])
@fetch_user_details
def medical_session_list(request, pk):
    patient = get_object_or_404(Patient, pk=pk, status='active', hospital_id=request.hospital.pk)

    is_paginated = False
    medical_sessions = None

    create_activity(request, 'GET', _('Patient Medical Sessions is fetched.'), check_activity_tag(request), patient)

    count = MedicalSession.objects.filter(patient=patient, status='active').count()

    sort_by = request.GET.get('sort')

    if sort_by not in ['asc', 'desc']:
        sort_by = 'desc'

    if sort_by == 'asc':
        medical_sessions = MedicalSession.objects.filter(
            patient=patient,
            status='active'
        ).select_related(
            'practitioner', 'hospital'
        ).order_by('created')
    elif sort_by == 'desc':
        medical_sessions = MedicalSession.objects.filter(patient=patient, status='active').select_related(
            'practitioner', 'hospital').order_by('-created')

    paginator = Paginator(medical_sessions, 30)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    if count > 30:
        is_paginated = True

    context = {
        'title': 'List | Medical Session',
        'patient': patient,
        'medical_session_count': count,
        'medical_sessions': medical_sessions,
        'page_obj': page_obj,
        'is_paginated': is_paginated,
    }

    return render(request, "medical_sessions/medical_session_list.html", context)


@login_required
@logged_in_user(['hospital level', 'practitioner level', 'nurse level'])
@fetch_user_details
def medical_session_detail(request, pk, suid):
    patient = get_object_or_404(Patient, pk=pk, hospital=request.hospital, status='active')

    medical_session = MedicalSession.objects.filter(
        uid=suid,
        status='active',
        hospital=request.hospital,
        patient=patient
    ).select_related(
        'practitioner',
        'department',
        'ward',
    ).first()

    if medical_session is None:
        return redirect('404.html')

    create_activity(request, 'GET', _('Patient Medical Session detail page is visited'), check_activity_tag(request),
                    patient)

    vsr = VitalSignRecord.objects.filter(
        status='active',
        medical_session=medical_session,
        patient=patient,
        hospital=request.hospital
    ).select_related(
        'nurse',
        'patient'
    ).order_by(
        '-created'
    )

    ioc = IntakeOutputChart.objects.filter(
        status='active',
        medical_session=medical_session,
        patient=patient,
        hospital=request.hospital
    ).select_related(
        'nurse',
        'patient'
    ).order_by(
        '-created'
    )

    notes = NurseNotes.objects.filter(
        status='active',
        medical_session=medical_session,
        patient=patient,
        hospital=request.hospital
    ).select_related(
        'nurse',
        'patient'
    ).order_by(
        '-created'
    )

    context = {
        'title': 'Detail | Medical Session',
        'medical_session': medical_session,
        'patient': patient,
        'ioc': ioc,
        'vsr': vsr,
        'notes': notes
    }

    return render(request, "medical_sessions/medical_session_detail.html", context)


@login_required
@logged_in_user(['reception level'])
@fetch_user_details
@check_token(['reception level'])
def reception_medical_session_create(request, pk):
    patient = get_object_or_404(Patient, id=pk, status='active', hospital=request.hospital)

    create_activity(request, 'GET', _('Medical session create page is visited'), 'Reception', patient)
    beds_occupied = MedicalSession.objects.filter(status='active', hospital=request.hospital, department__name="IPD",
                                                  ipd_status='Occupied').count()
    beds_available = request.hospital.beds - beds_occupied

    if request.method == 'POST':
        reception_medical_session_form = forms.NewReceptionMedicalSessionForm(request.POST or None)
        ms_record = None  # ms= medical session
        if reception_medical_session_form.is_valid():
            if reception_medical_session_form.cleaned_data.get('department') == 'IPD':
                ms_record = MedicalSession.objects.filter(
                    status='active', hospital=request.hospital, department__name="IPD",
                    ipd_status='Occupied', patient=Patient
                ).first()
            try:
                with transaction.atomic():
                    if ms_record:
                        ms_record.ipd_status = 'Not Applicable'

                    medical_session = reception_medical_session_form.save(commit=False)
                    medical_session.hospital = request.hospital
                    medical_session.patient = patient
                    medical_session.ipd_status = 'Occupied'
                    medical_session.creator_user = request.user
                    medical_session.creation_place = "Reception"
                    medical_session.save()

                messages.success(request, _('New medical session created.'))
                create_activity(request, 'INSERT', _('Patient Medical Sessions is created at reception.'), 'Reception',
                                patient)
                return redirect(reverse('receptions:ms-detail', args=(pk, medical_session.pk)))
            except DatabaseError:
                messages.error(request, _('Something went wrong.'))
        else:
            messages.error(request, _('Something went wrong. Check the errors.'))
    else:
        reception_medical_session_form = forms.NewReceptionMedicalSessionForm()

    context = {
        'title': 'New Medical Session | Reception',
        'hospital_user': True,
        'reception_medical_session_form': reception_medical_session_form,
        'hospital_name': request.hospital.name,
        'patient': patient,
        'beds_available': beds_available,
    }

    return render(request, "medical_sessions/reception_medical_session_create.html", context)
