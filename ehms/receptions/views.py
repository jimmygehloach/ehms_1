import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.utils.dateparse import parse_datetime
from django.views.generic import ListView, TemplateView

from ehms.activities.views import create_activity, cam
from ehms.core.decorators import logged_in_user, fetch_user_details
from ehms.core.utils import check_activity_level, kurrent_timestamp, is_valid_uuid, verhoeff_random_number
from ehms.medical_sessions.models import MedicalSession
from ehms.patients.models import Patient, PatientImage
from ehms.receptions.models import Reception
from ehms.utils.helpers import UTL


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ReceptionListView(ListView):
    """
    Return the list of receptions exist in the hospital
    """
    model = Reception
    template_name = 'receptions/reception_list.html'
    context_object_name = 'reception_list'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(hospital=self.request.hospital.pk, status='active')
        queryset = queryset.order_by(UTL.fetch_sort_basic(self.request.GET.get('sort'), 'created'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: fix this function
        create_activity(self.request, 'GET', cam().get('reception_list_page'),
                        check_activity_level(self.request))

        context['title_check'] = 'Reception List'
        context['title'] = 'Receptions | Hospital'

        return context


@login_required
@logged_in_user(['hospital level'])
@fetch_user_details
def reception_token_request_page(request):
    create_activity(request, 'GET', _('Reception token page is fetched.'), check_activity_level(request))
    receptions = Reception.objects.filter(hospital=request.hospital, status='active', )
    receptions = UTL.fetch_sorted_query(receptions, request.GET.get('sort', ''), 'created')
    paginator = UTL.view_pagination(receptions, request.GET.get('page', 1), 10)

    if request.method == 'POST':
        if 'reception' in request.POST and 'token_timestamp' in request.POST:
            reception_id = request.POST.get('reception')
            timestamp_data = request.POST.get('token_timestamp')
            UTL.custom_print(not reception_id)
            UTL.custom_print(not timestamp_data)
            if timestamp_data != "" and reception_id != "":
                timestamp_pattern = re.compile(r'^(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2})$')
                if timestamp_pattern.match(timestamp_data):
                    if parse_datetime(timestamp_data).timestamp() > kurrent_timestamp():
                        try:
                            reception = Reception.objects.get(pk=reception_id, status='active')
                        except Reception.DoesNotExist:
                            reception = None

                        if reception:
                            try:
                                with transaction.atomic():
                                    reception.token = verhoeff_random_number(1, 8)
                                    reception.token_timestamp = request.POST.get('token_timestamp')
                                    reception.verify_token = False
                                    reception.save()
                                    messages.success(request, _('Token generated.'))
                                    message = _('Reception token is generated. Name: - %(name)s.') % {
                                        'name': reception.name, }
                                    create_activity(request, 'INSERT', message, check_activity_level(request))
                                    return redirect(reverse('receptions:token'))
                            except Exception as e:
                                messages.error(request, _('Something went wrong.'))
                        else:
                            messages.error(request, _('Invalid reception id. Try again.'))
                    else:
                        messages.error(request, _('You cannot assign previous date time. Try again.'))
                else:
                    messages.error(request, _('Invalid date time of token. Try again.'))
            else:
                messages.error(request, _('Invalid data send. Check both the fields and try again.'))
        else:
            messages.error(request, _('Something went wrong. Try again.'))

    data_send = {
        'title': 'Token | Practitioners',
        'page_obj': paginator.get('page_obj', None),
        'is_paginated': paginator.get('is_paginated', None),
        'reception_count': paginator.get('count', None),
    }

    return render(request, 'receptions/login_token.html', data_send)


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['reception level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ReceptionDashboardTemplateView(TemplateView):
    template_name = 'receptions/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        create_activity(self.request, 'GET', _('Reception dashboard is fetched.'), check_activity_level(self.request))
        today = timezone.now().astimezone(timezone.get_current_timezone())

        context["title"] = 'Dashboard | Reception',
        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['reception level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ReceptionProfileTemplateView(TemplateView):
    template_name = 'receptions/profile.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['reception level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ReceptionNewMSDetailTemplateView(TemplateView):
    template_name = 'receptions/new-medical-session-detail.html'

    def get_context_data(self, **kwargs):
        medical_session = None
        context = super().get_context_data(**kwargs)

        p_id = self.kwargs.get('p_id')
        ms_id = self.kwargs.get('ms_id')

        patient = get_object_or_404(Patient, id=p_id, status='active')
        medical_session = []
        try:
            medical_session = MedicalSession.objects.filter(
                id=ms_id, status='active', hospital=self.request.hospital, patient=patient
            ).select_related('practitioner', 'department', 'ward', 'patient').prefetch_related(
                Prefetch(
                    'patient__patient_image',
                    PatientImage.objects.filter(status='active', current_image=True),
                    "current_photo"
                )
            ).first()
        except Exception as e:
            messages.error(self.request, 'Something went wrong. Try again later.')

        create_activity(self.request, 'GET', _('Reception medical session detail is fetched.'),
                        check_activity_level(self.request))

        context["title"] = 'MS Detail | Reception'
        context["medical_session"] = medical_session
        return context
