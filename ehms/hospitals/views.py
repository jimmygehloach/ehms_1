from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, TemplateView

from ehms.activities.models import Activity
from ehms.activities.views import create_activity, cam
from ehms.core.decorators import logged_in_user, fetch_user_details
from ehms.core.utils import check_activity_level
from ehms.hospitals.forms import (
    HospitalGeneralInfo, HospitalLocationInfo, HospitalContactInfo, HospitalAddressInfo,
    HospitalRepresentativeForm, HospitalUserForm
)
from ehms.hospitals.models import HospitalRepresentative
from ehms.medical_sessions.models import MedicalSession, Department, Ward
from ehms.nurses.models import NurseHospital, Nurse
from ehms.patients.models import Patient, PatientImage
from ehms.practitioners.models import PractitionerHospital, Practitioner
from ehms.utils.helpers import UTL

User = get_user_model()


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class ActivityListView(ListView):
    """
    Return the list of activities performed in the hospital sections
    """
    model = Activity
    template_name = 'hospitals/hospital_activities.html'
    context_object_name = 'activity_list'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(hospital=self.request.hospital.pk, status='active')
        queryset = queryset.order_by(UTL.fetch_sort_basic(self.request.GET.get('sort'), 'created'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: fix this function
        create_activity(self.request, 'GET', cam().get('activity_page'),
                        check_activity_level(self.request))

        context['title_check'] = 'activity'
        context['title'] = 'Activities | Hospital'

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level', 'practitioner level', 'nurse level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class HospitalMedicalSessionListView(ListView):
    """
    Return the list of medical sessions taken place in current hospital
    """
    model = MedicalSession
    template_name = 'hospitals/hospital_medical_sessions.html'
    context_object_name = 'medical_session_list'
    paginate_by = 30

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(
            status='active',
            hospital_id=self.request.hospital.pk,
            patient__status='active',
        ).select_related('patient', 'practitioner').prefetch_related(
            Prefetch(
                'patient__patient_image',
                PatientImage.objects.filter(status='active', current_image=True),
                "current_photo"
            )
        )
        queryset = queryset.order_by(UTL.fetch_sort_basic(self.request.GET.get('sort'), 'created'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TODO: fix this function
        create_activity(self.request, 'GET', cam().get('hospital_ms_page'), check_activity_level(self.request))
        context['title'] = 'Medical Sessions | Hospital'

        # TODO: hospital_medical_session_count // look into this ?

        return context


@login_required
@logged_in_user(['hospital level'])
@fetch_user_details
def hospital_dashboard(request):  # TODO: convert this later on to some class Based View
    create_activity(request, 'GET', _('Hospital dashboard is fetched.'), check_activity_level(request))
    context = {}
    context['total_patients'] = Patient.objects.filter(hospital=request.hospital,).count()
    context['total_medical_sessions'] = MedicalSession.objects.filter(hospital=request.hospital).count()
    context['total_practitioners'] = Practitioner.objects.filter(practitioner_hospital__hospital=request.hospital,
                                                      practitioner_hospital__current_hospital=True).distinct().count()

    context['total_nurses'] = Nurse.objects.filter(hospital_belong_to_nurse__hospital=request.hospital,
                                        hospital_belong_to_nurse__current_hospital=True).distinct().count()

    context['patient_ipd'] = MedicalSession.objects.filter(
        hospital_id=request.hospital.pk, status='active', department__name='IPD').count()

    context['patient_opd'] = MedicalSession.objects.filter(
        hospital_id=request.hospital.pk, status='active', department__name='OPD').count()

    context['beds_occupied'] = MedicalSession.objects.filter(
        status='active', hospital=request.hospital, ipd_status='Occupied').count()
    context['beds_available'] = request.hospital.beds - context["beds_occupied"]

    context['medical_sessions_department_wise'] = MedicalSession.objects.filter(
        hospital=request.hospital, status='active'
    ).select_related('department', 'patient', 'practitioner').order_by('-created')[:10]

    context['medical_sessions_ward_wise'] = MedicalSession.objects.filter(
        hospital=request.hospital, status='active'
    ).select_related('department', 'patient', 'practitioner').order_by('-created')[:10]

    context['valid_departments'] = Department.objects.filter(status='active', hospital=request.hospital)
    context['valid_wards'] = Ward.objects.filter(status='active', hospital=request.hospital)


    context['title'] = 'Dashboard | Hospital'

    if request.method == 'POST':
        if request.POST.get('end_date') and request.POST.get('start_date') and request.POST.get('department'):
            department = request.POST.get('department')
            if context["valid_departments"].filter(name=department).exists():
                context["medical_sessions_department_wise"] = MedicalSession.objects.filter(
                    hospital_id=request.hospital.pk,
                    department__name=department,
                    status='active',
                    created__range=[request.POST['start_date'], request.POST['end_date']]
                ).select_related('department', 'patient', 'practitioner').order_by('-created')[:10]
                messages.success(request, UTL.success_message('HOSPITAL_DEPARTMENT_DASHBOARD'))
            else:
                messages.error(request, UTL.error_message('DB_EX_ER'))
            return redirect(reverse('hospitals:hospital-dashboard'))
        elif request.POST.get('end_date') and request.POST.get('start_date') and request.POST.get('ward'):
            ward = request.POST.get('ward')
            if context["valid_wards"].filter(name=ward).exists():
                context["medical_sessions_ward_wise"] = MedicalSession.objects.filter(
                    hospital_id=request.hospital.pk,
                    ward__name=ward,
                    status='active',
                    created__range=[request.POST['start_date'], request.POST['end_date']]
                ).select_related('ward', 'patient', 'practitioner').order_by('-created')[:10]
                messages.success(request, UTL.success_message('HOSPITAL_RANGE_DASHBOARD'))
            else:
                messages.error(request, UTL.error_message('DB_EX_ER'))
            return redirect(reverse('hospitals:hospital-dashboard'))
        else:
            messages.error(request, UTL.error_message('BOTH_DATES_REQUIRED'))
            return redirect(reverse('hospitals:hospital-dashboard'))

    return render(request, "hospitals/dashboard.html", context)


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
class HospitalProfileTemplateView(TemplateView):
    template_name = 'hospitals/hospital_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        create_activity(self.request, 'GET', _('Hospital profile is fetched.'), check_activity_level(self.request))

        representatives = HospitalRepresentative.objects.filter(
            status='active', hospital=self.request.hospital).order_by('-created')

        hospital_users = User.objects.filter(
            is_active=True, userprofile__user_unique_id=self.request.hospital.uid
        ).select_related('userprofile').order_by('-date_joined')

        context["title"] = "Profile | Hospital"
        context["hospital_general_info"] = HospitalGeneralInfo(instance=self.request.hospital)
        context["hospital_location_info"] = HospitalLocationInfo(instance=self.request.hospital)
        context["hospital_contact_info"] = HospitalContactInfo(instance=self.request.hospital)
        context["hospital_address_info"] = HospitalAddressInfo(instance=self.request.hospital)
        context["representatives"] = representatives
        context["hospital_users"] = hospital_users

        return context
