import re
import string
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.db import transaction, DatabaseError
from django.db.models import Prefetch
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from ehms.core.decorators import logged_in_user, fetch_user_details, check_token
from ehms.core.utils import check_activity_level, kurrent_timestamp, is_valid_uuid, verhoeff_random_number
from ehms.patients.models import PatientImage
from ehms.practitioners.models import PractitionerHospital, Practitioner
from ehms.activities.views import create_activity
from ehms.medical_sessions.models import MedicalSession
from ehms.utils.helpers import UTL


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class PractitionerHospitalListView(ListView):
    model = Practitioner
    template_name = 'practitioners/practitioner_in_hospital_list.html'
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        create_activity(self.request, 'GET', _('Practitioner hospital list viewed'), check_activity_level(self.request))
        return context

    def get_queryset(self):
        return Practitioner.objects.filter(practitioner_hospital__hospital=self.request.hospital, status='active',
                                           practitioner_hospital__status='active',
                                           practitioner_hospital__current_hospital=True, ).distinct()


@login_required
@logged_in_user(['hospital level', 'practitioner level', 'nurse level'])
@fetch_user_details
def practitioner_profile_page(request, pk):
    instance = get_object_or_404(Practitioner, pk=pk, status='active')

    create_activity(
        request,
        'GET',
        _('Practitioner profile is fetched with uid: %(p)s') % {'p': instance.uid},
        check_activity_level(request)
    )

    practitioner_hospitals = PractitionerHospital.objects.filter(
        practitioner_id=instance.pk,
        practitioner__status='active',
        status='active',
    ).select_related('hospital')

    return render(request, 'practitioners/practitioner_detail.html', {
        'practitioner': instance,
        'title': 'Profile | Practitioner',
        'practitioner_hospitals': practitioner_hospitals,
    })


@login_required
@logged_in_user(['practitioner level'])
@fetch_user_details
def practitioner_dashboard(request):
    instance = get_object_or_404(Practitioner, pk=request.practitioner.pk, status='active')
    today = timezone.now().astimezone(timezone.get_current_timezone())
    create_activity(request, 'GET', _('Practitioner\'s dashboard page is fetched.'), check_activity_level(request))

    sessions = MedicalSession.objects.filter(practitioner=instance.pk, status='active').count()
    today_sessions = MedicalSession.objects.filter(practitioner=instance.pk, status='active', created__year=today.year,
                                                   created__month=today.month, created__day=today.day, ).count()

    return render(request, 'practitioners/dashboard.html', {
        'total_sessions': sessions,
        'today_sessions': today_sessions,
        'practitioner': instance,
        'title': 'Dashboard | Practitioner',
    })


@login_required
@logged_in_user(['hospital level'])
@fetch_user_details
def practitioner_token_request_page(request):
    _sort_by = ''
    is_paginated = False
    _practitioners = []

    create_activity(request, 'GET', _('Practitioners token page is fetched.'), check_activity_level(request))

    _practitioners = PractitionerHospital.objects.filter(
        hospital_id=request.hospital,
        status='active',
        current_hospital=True,
        practitioner__status='active'
    ).select_related('practitioner')

    _sort_by = request.GET.get('sort')

    if _sort_by not in ['asc', 'desc']:
        _sort_by = 'desc'

    if _sort_by == 'asc':
        _practitioners = _practitioners.order_by('created')
    elif _sort_by == 'desc':
        _practitioners = _practitioners.order_by('-created')

    paginator = Paginator(_practitioners, 30)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if paginator.count > 30:
        is_paginated = True

    if request.method == 'POST':
        instance = get_object_or_404(Practitioner, pk=request.POST.get('practitioner'), status='active')

        if 'practitioner' in request.POST and 'token_timestamp' in request.POST:
            practitioner_data = request.POST['practitioner']
            timestamp_data = request.POST['token_timestamp']

            if timestamp_data != '' and practitioner_data != '':
                timestamp_pattern = re.compile(r'^(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2})$')
                if timestamp_pattern.match(timestamp_data):
                    if parse_datetime(timestamp_data).timestamp() > kurrent_timestamp():
                        try:
                            practitioner = Practitioner.objects.filter(pk=practitioner_data,
                                                                       status='active').first()
                        except Practitioner.DoesNotExist:
                            practitioner = None
                        if practitioner:
                            try:
                                with transaction.atomic():
                                    practitioner.token = verhoeff_random_number(1, 8)
                                    practitioner.token_timestamp = request.POST.get('token_timestamp')
                                    practitioner.verify_token = False
                                    practitioner.save()
                                    messages.success(request, _('Token generated.'))

                                    practitioner_name = practitioner.first_name + ' ' + practitioner.last_name
                                    message = _('Nurse token is generated. Name: - %(name)s.') % {
                                        'name': practitioner_name, }
                                    create_activity(request, 'INSERT', message, check_activity_level(request))
                                    return redirect(reverse('practitioners:token'))
                            except DatabaseError:
                                messages.error(request, _('Something went wrong.'))
                        else:
                            messages.error(request, _('Something happened wrong. Try again.'))

                    else:
                        messages.error(request, _('You cannot assign previous date time. Try again.'))
                else:
                    messages.error(request, _('Invalid date time of token. Try again.'))
            else:
                messages.error(request, _('Invalid data send. Check both the fields and try again.'))
        else:
            messages.error(request, _('Something went wrong. Try again.'))

    data_send = {
        'page_obj': page_obj,
        'is_paginated': is_paginated,
        'practitioners_count': paginator.count,
        'title': 'Token | Practitioners',
    }

    return render(request, 'practitioners/login_token.html', data_send)


@login_required
@logged_in_user(['hospital level', 'practitioner level', 'nurse level'])
@fetch_user_details
@check_token(['practitioner level', 'nurse level'])
def practitioner_medical_session_list(request, pk):
    practitioner = get_object_or_404(Practitioner, pk=pk, status='active')
    create_activity(
        request, 'GET',
        _(f"Practitioner medical session list fetched with uid: {practitioner.first_name} {practitioner.last_name}"),
        check_activity_level(request)
    )

    practitioner_ms = MedicalSession.objects.filter(
        hospital_id=request.hospital.pk, status='active',
        practitioner=practitioner,
        practitioner__status='active',
        patient__status='active',
    ).select_related('practitioner', 'patient').prefetch_related(
        Prefetch("patient__patient_image", PatientImage.objects.filter(status='active', current_image=True), "current_photo")
    )
    practitioner_ms = UTL.fetch_sorted_query(practitioner_ms, request.GET.get('sort', ''), 'created')
    paginator = UTL.view_pagination(practitioner_ms, request.GET.get('page', 1), 30)

    context = {
        'title': 'Medical Sessions | Practitioner',
        'page_obj': paginator.get('page_obj', None),
        'is_paginated': paginator.get('is_paginated', None),
        'patient_count': paginator.get('count', None),
        'practitioner': practitioner,
    }

    return render(request, 'practitioners/practitioner_medical_sessions_list.html', context)
