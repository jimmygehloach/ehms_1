import traceback

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction, DatabaseError
from django.db.models import Q, Count, Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, UpdateView

from ehms.activities.views import create_activity, cam
from ehms.core.utils import check_activity_level
from ehms.medical_sessions.models import MedicalSession, Keyword
from ehms.patients.forms import (
    NewPatientRegistrationForm, NewPatientAddressForm,
    UpdatePatientHospitalForm, PatientDocumentUploadForm, UpdatePatientGeneralInfo, UpdatePatientPersonalInfo,
    UpdatePatientPhysicalInfo, UpdatePatientMedicalInfo, UpdatePatientImportantInfo, UpdatePatientMiscInfo,
    UpdatePatientImmunizationInfo, UpdatePatientFemaleInfo, PatientImageUploadForm, PatientDeathRecordForm
)
from ehms.patients.models import Patient, HealthStatus, PatientDocument, PatientAddress, PatientImage

from ehms.addresses.models import Country, Region, District, Town, Postcode
from ehms.core.decorators import logged_in_user, fetch_user_details, check_token
from ehms.utils.helpers import UTL


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['hospital level', 'practitioner level', 'nurse level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
@method_decorator(check_token(['practitioner level', 'nurse level']), name='dispatch')
class PatientListView(ListView):
    """
    Return the list of patient filtered by hospital
    """
    model = Patient
    template_name = 'patients/patients_list.html'
    context_object_name = 'patient_list'
    paginate_by = 30

    def get_queryset(self):
        queryset = super(PatientListView, self).get_queryset()

        queryset = queryset.filter(
            status='active', patient_image__current_image=True
        ).select_related('health_status').prefetch_related(
            Prefetch("patient_image", PatientImage.objects.filter(status='active', current_image=True), "current_photo")
        )
        queryset = queryset.order_by(UTL.fetch_sort_basic(self.request.GET.get('sort'), 'created'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(PatientListView, self).get_context_data(**kwargs)

        # TODO: fix this function
        create_activity(self.request, 'GET', _('Patient list page visited.'), check_activity_level(self.request))

        context['title'] = 'List | Patients'

        return context


@method_decorator(login_required, name='dispatch')
@method_decorator(logged_in_user(['reception level']), name='dispatch')
@method_decorator(fetch_user_details, name='dispatch')
@method_decorator(check_token(['reception level']), name='dispatch')
class PatientReceptionListView(ListView):
    """
    Return the list of patient filtered by hospital
    """
    model = Patient
    template_name = 'patients/patients_reception_list.html'
    context_object_name = 'patient_list'
    paginate_by = 30

    def get_queryset(self):
        queryset = super(PatientReceptionListView, self).get_queryset()

        queryset = queryset.filter(
            status='active', hospital=self.request.hospital, vital_status=True
        ).prefetch_related(
            Prefetch("patient_image", PatientImage.objects.filter(status='active', current_image=True), "current_photo")
        )

        queryset = queryset.only('pk', 'uid', 'first_name', 'middle_name', 'last_name', )
        queryset = queryset.order_by(UTL.fetch_sort_basic(self.request.GET.get('sort'), 'created'))

        return queryset

    def get_context_data(self, **kwargs):
        context = super(PatientReceptionListView, self).get_context_data(**kwargs)

        # TODO: fix this function
        create_activity(self.request, 'GET', _('Patient list page visited.'), check_activity_level(self.request))

        context['title'] = 'List | Patients'

        return context


@login_required
@logged_in_user(['hospital level'])
@fetch_user_details
def patient_create(request):
    if request.method == 'POST':
        patient_form = NewPatientRegistrationForm(request.POST or None)
        patient_image_upload_form = PatientImageUploadForm(request.POST or None, request.FILES or None)
        patient_address_form = NewPatientAddressForm(request.POST or None)

        if patient_form.is_valid() and patient_image_upload_form.is_valid() and patient_address_form.is_valid():
            try:
                with transaction.atomic():
                    patient = patient_form.save(commit=False)
                    patient.hospital = request.hospital
                    patient.creator_user = request.user
                    patient.save()
                    patient_form.save_m2m()

                    patient_address = patient_address_form.save(commit=False)
                    patient_address.patient = patient
                    patient_address.hospital = request.hospital
                    patient_address.creator_user = request.user
                    patient_address.save()

                    patient_image_upload = patient_image_upload_form.save(commit=False)
                    patient_image_upload.patient = patient
                    patient_image_upload.current_image = True
                    patient_image_upload.hospital = request.hospital
                    patient_image_upload.creator_user = request.user
                    patient_image_upload.save()

                    create_activity(request, 'INSERT', cam().get('new_patient'), check_activity_level(request), patient)
                    messages.success(request, UTL.success_message('PATIENT_REGISTER'))
                    return redirect(reverse('patients:create'))
            except DatabaseError as e:
                UTL.custom_print(e)
                UTL.custom_print(traceback.format_exc())
                messages.error(request, UTL.error_message('DB_EX_ER'))

        else:
            messages.error(request, _('Something went wrong.'))

    else:
        patient_form = NewPatientRegistrationForm()
        patient_address_form = NewPatientAddressForm()
        patient_image_upload_form = PatientImageUploadForm()

    data_send = {
        'title': 'Patient Registration',
        'total_patient_registered': Patient.objects.filter(hospital_id=request.hospital.pk).count(),
        'patient_form': patient_form,
        'patient_address_form': patient_address_form,
        'patient_image_upload_form': patient_image_upload_form,
    }

    return render(request, "patients/patient_create.html", data_send)


@login_required
@logged_in_user(['hospital level', 'practitioner level'])
@fetch_user_details
@check_token(['practitioner level'])
def edit_patient_address(request, pk, pa):
    # check the patient
    patient = get_object_or_404(Patient, pk=pk, status='active', hospital=request.hospital)

    # check the address
    address_element = get_object_or_404(PatientAddress, pk=pa, status='active', patient=patient,
                                        hospital=request.hospital)

    # create an activity
    create_activity(request, 'GET', _('Patient edit address page is fetched.'), check_activity_level(request), patient)

    # Post Section
    if request.method == 'POST':
        patient_address_form = NewPatientAddressForm(request.POST or None, instance=address_element)
        if patient_address_form.is_valid():
            try:
                with transaction.atomic():
                    # Save the address
                    patient_address_form.save()
                    messages.success(request, _('Patient address updated.'))

                    # create an activity
                    create_activity(request, 'UPDATE', _('Patient address updated.'), check_activity_level(request),
                                    patient)

                    return redirect(reverse('patients:detail', args=(pk,)))
            except DatabaseError:
                messages.error(request, _('Something went wrong.'))
        else:
            messages.error(request, _('Something went wrong.'))
    else:
        patient_address_form = NewPatientAddressForm(instance=address_element)

    data_send = {
        'patient_address_form': patient_address_form,
        'patient': patient,
        'title': 'Edit Address | Patient',
    }

    return render(request, 'patients/edit_patient_address.html', data_send)


@login_required
@logged_in_user(['hospital level', 'practitioner level', 'nurse level'])
@fetch_user_details
@check_token(['practitioner level', 'nurse level'])
def patient_detail(request, pk):
    """
    Patient profile view

    :param request: WSGI request
    :param pk: primary key of the patient
    :return: nothing
    """
    # TODO :

    # patient check
    patient = get_object_or_404(Patient, pk=pk, status='active')

    # create new activity
    create_activity(
        request,
        'GET',
        _('Patient profile page is accessed.'),
        check_activity_level(request),
        patient
    )

    # health status name list
    health_status = HealthStatus.objects.all()

    # patient document list
    patient_documents = PatientDocument.objects.filter(patient_id=pk, status='active')

    # patient address list
    patient_addresses = PatientAddress.objects.filter(patient_id=pk, status='active')

    patient_image = PatientImage.objects.filter(patient_id=pk, current_image=True, status='active').first()

    # modal forms required in this view
    # # forms which are going to update
    # ## Outsider form: form for other hospitals where the current patient is not registered
    update_patient_hospital_form = UpdatePatientHospitalForm(instance=patient)

    # ## Insider form: form for the hospital where current patient is registered
    update_patient_general_info = UpdatePatientGeneralInfo(instance=patient)
    update_patient_personal_info = UpdatePatientPersonalInfo(instance=patient)
    update_patient_physical_info = UpdatePatientPhysicalInfo(instance=patient)
    update_patient_medical_info = UpdatePatientMedicalInfo(instance=patient)
    update_patient_important_info = UpdatePatientImportantInfo(instance=patient)
    update_patient_misc_info = UpdatePatientMiscInfo(instance=patient)
    update_patient_immunization_info = UpdatePatientImmunizationInfo(instance=patient)
    update_patient_female_info = UpdatePatientFemaleInfo(instance=patient)

    # # forms which are going to create
    patient_document_upload_form = PatientDocumentUploadForm()
    new_patient_address_form = NewPatientAddressForm()

    if request.method == 'POST':
        # This section is for other hospitals (where current patient is not registered) to see and perform some actions
        if patient.hospital != request.hospital and request.group_name in 'hospital level,practitioner level':
            if 'update_patient_hospital' in request.POST:
                update_patient_hospital_form = UpdatePatientHospitalForm(request.POST or None, instance=patient)
                if update_patient_hospital_form.is_valid():
                    try:
                        with transaction.atomic():
                            # patient hospital changed
                            update_patient_hospital_form.save()
                            messages.success(request, _('Patient hospital saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'UPDATE',
                                _('Patient hospital updated.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))

        # This section is for hospital (where current patient is registered) to see and perform some actions
        elif patient.hospital == request.hospital and request.group_name in 'hospital level,practitioner level':
            if 'update_patient_general_info' in request.POST:
                update_patient_general_info = UpdatePatientGeneralInfo(request.POST or None, instance=patient)
                if update_patient_general_info.is_valid():
                    try:
                        with transaction.atomic():
                            # patient general information updated
                            update_patient_general_info.save()
                            messages.success(request, _('Patient general information saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'UPDATE',
                                _('Patient general information updated.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))
            elif 'update_patient_personal_info' in request.POST:
                update_patient_personal_info = UpdatePatientPersonalInfo(request.POST or None, instance=patient)
                if update_patient_personal_info.is_valid():
                    try:
                        with transaction.atomic():
                            # patient personal information updated
                            update_patient_personal_info.save()
                            messages.success(request, _('Patient personal information saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'UPDATE',
                                _('Patient personal information updated.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))
            elif 'update_patient_physical_info' in request.POST:
                update_patient_physical_info = UpdatePatientPhysicalInfo(request.POST or None, instance=patient)
                if update_patient_physical_info.is_valid():
                    try:
                        with transaction.atomic():
                            # patient physical information updated
                            update_patient_physical_info.save()
                            messages.success(request, _('Patient physical information saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'UPDATE',
                                _('Patient physical information updated.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))
            elif 'update_patient_medical_info' in request.POST:
                update_patient_medical_info = UpdatePatientMedicalInfo(request.POST or None, instance=patient)
                if update_patient_medical_info.is_valid():
                    try:
                        with transaction.atomic():
                            # patient medical information updated
                            update_patient_medical_info.save()
                            messages.success(request, _('Patient medical information saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'UPDATE',
                                _('Patient medical information updated.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))
            elif 'update_patient_important_info' in request.POST:
                update_patient_important_info = UpdatePatientImportantInfo(request.POST or None, instance=patient)
                if update_patient_important_info.is_valid():
                    try:
                        with transaction.atomic():
                            # patient important information updated
                            update_patient_important_info.save()
                            messages.success(request, _('Patient important information saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'UPDATE',
                                _('Patient important information updated.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))
            elif 'update_patient_misc_info' in request.POST:
                update_patient_misc_info = UpdatePatientMiscInfo(request.POST or None, instance=patient)
                if update_patient_misc_info.is_valid():
                    try:
                        with transaction.atomic():
                            # patient misc. information updated
                            update_patient_misc_info.save()
                            messages.success(request, _('Patient misc information saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'UPDATE',
                                _('Patient misc information updated.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))
            elif 'update_patient_immunization_info' in request.POST:
                update_patient_immunization_info = UpdatePatientImmunizationInfo(request.POST or None, instance=patient)
                if update_patient_immunization_info.is_valid():
                    try:
                        with transaction.atomic():
                            # patient immunization info updated
                            update_patient_immunization_info.save()
                            messages.success(request, _('Patient immunization information saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'UPDATE',
                                _('Patient immunization information updated.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))
            elif 'update_patient_female_info' in request.POST:
                update_patient_female_info = UpdatePatientFemaleInfo(request.POST or None, instance=patient)
                if update_patient_female_info.is_valid():
                    try:
                        with transaction.atomic():
                            # female patient information updated
                            update_patient_female_info.save()
                            messages.success(request, _('Patient female information saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'UPDATE',
                                _('Patient female information updated.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))
            elif 'patient_document_upload' in request.POST:
                patient_document_upload_form = PatientDocumentUploadForm(request.POST or None)
                if patient_document_upload_form.is_valid():
                    try:
                        with transaction.atomic():
                            # patient document uploaded
                            patient_document_upload_form.save()
                            messages.success(request, _('Patient document saved.'))

                            # create new activity
                            create_activity(
                                request,
                                'INSERT',
                                _('Patient document uploaded.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))
            elif 'new_patient_address_form' in request.POST:
                new_patient_address_form = NewPatientAddressForm(request.POST or None)
                if new_patient_address_form.is_valid():
                    try:
                        with transaction.atomic():
                            # patient new address created
                            x = new_patient_address_form.save(commit=False)
                            x.patient = patient
                            x.creator_user = request.user
                            x.hospital = request.hospital
                            x.save()
                            messages.success(request, _('Patient new address created.'))

                            # create new activity
                            create_activity(
                                request,
                                'INSERT',
                                _('Patient new address created.'),
                                check_activity_level(request),
                                patient
                            )
                            return redirect('patients:detail', pk=pk)
                    except DatabaseError:
                        messages.error(request, _('Something went wrong.'))
                else:
                    messages.error(request, _('Something went wrong.'))

    data_send = {
        'patient': patient,
        'patient_image': patient_image,
        'update_patient_general_info': update_patient_general_info,
        'update_patient_hospital_form': update_patient_hospital_form,
        'update_patient_personal_info': update_patient_personal_info,
        'update_patient_physical_info': update_patient_physical_info,
        'update_patient_medical_info': update_patient_medical_info,
        'update_patient_important_info': update_patient_important_info,
        'update_patient_misc_info': update_patient_misc_info,
        'update_patient_immunization_info': update_patient_immunization_info,
        'update_patient_female_info': update_patient_female_info,
        'patient_document_upload_form': patient_document_upload_form,
        'new_patient_address_form': new_patient_address_form,
        'health_statuses': health_status,
        'patient_documents': patient_documents,
        'patient_addresses': patient_addresses,
        'title': 'Profile | Patient',
    }

    return render(request, 'patients/patient_detail.html', data_send)


@login_required
@logged_in_user(['hospital level', 'practitioner level', 'reception level', 'nurse level'])
@fetch_user_details
@check_token(['practitioner level', 'nurse level', 'reception level'])
def patient_search_list(request):
    page_obj = None
    search_word = request.GET.get('search')
    if request.method == 'GET' and 'search' in request.GET:
        if not search_word:
            return redirect(reverse("patients:list"))
        else:
            try:
                filters = []
                filters.append(Q(uid__exact=search_word))
                filters.append(UTL.custom_print(UTL.name_filter_query(search_word)))
                query = Patient.objects.filter(
                    Q(uid__exact=search_word) |
                    Q(first_name__icontains=search_word) |
                    Q(middle_name__icontains=search_word) |
                    Q(last_name__icontains=search_word),
                    status='active',
                    hospital=request.hospital
                ).prefetch_related(
                    Prefetch('patient_image', PatientImage.objects.filter(status='active', current_image=True), "current_photo")
                )

                patients = UTL.fetch_sorted_query(query, request.GET.get('sort'), 'created')
                paginator = UTL.view_pagination(patients, request.GET.get('page', 1), 30)
                page_obj = paginator.get('page_obj')

                message = _('Patient record is searched with: - %(w)s .Check other columns for more detail.'
                        ) % {'w': search_word}
                create_activity(request, 'GET', message, check_activity_level(request))
                if paginator.get('count', 0) > 0:
                    messages.success(request, UTL.success_message('ADVANCED_SEARCH'))
                else:
                    messages.success(request, UTL.success_message('ADVANCED_SEARCH_NOT'))
            except Exception as e:
                UTL.custom_print(traceback.format_exc())
                messages.error(request, UTL.error_message('DB_EX_ER'))

    context = {
        'search_word': search_word,
        'title': 'Search | Patient',
        'keywords': Keyword.objects.filter(status='active'),
        'page_obj': page_obj,
    }

    return render(request, "patients/patient_search_list.html", context)


@login_required
@logged_in_user(['hospital level', 'practitioner level'])
@fetch_user_details
@check_token(['practitioner level'])
def patient_advanced_search_list(request):
    search_option = request.GET.get('search_option')
    page_obj = None

    if request.method == 'GET':

        if 'search_option' in request.GET and search_option:

            if search_option == 'patient_name' and request.GET.get('patient_name_or_blood_group') != '':
                filters = []
                if result := UTL.name_filter_query(request.GET.get('patient_name_or_blood_group')):
                    filters.extend(result)
                if result := UTL.address_filter_query(request.GET.get('country'), request.GET.get('region'),
                                                      request.GET.get('district'), request.GET.get('town'),
                                                      request.GET.get('postcode')):
                    filters.extend(result)
                try:
                    query_by_name = Patient.objects.filter(status='active', hospital=request.hospital,
                                                           *filters).distinct()
                    message = f"Patient record is searched (advanced) with Country: {request.GET.get('country', '')}," \
                              f"Region: {request.GET.get('region', '')}, District: {request.GET.get('district', '')}," \
                              f"Town: {request.GET.get('town', '')}, Postcode: {request.GET.get('postcode', '')}," \
                              f"Patient name: {request.GET.get('patient_name_or_blood_group')}." \
                              f"Look into other columns for more information."

                    create_activity(request, 'GET', message, check_activity_level(request))
                    patients = UTL.fetch_sorted_query(query_by_name, request.GET.get('sort'), 'created')
                    paginator = UTL.view_pagination(patients, request.GET.get('page', 1), 30)
                    page_obj = paginator.get('page_obj')

                    if paginator.get('count', 0) > 0:
                        messages.success(request, UTL.success_message('ADVANCED_SEARCH'))
                    else:
                        messages.success(request, UTL.success_message('ADVANCED_SEARCH_NOT'))
                except Exception as e:
                    UTL.custom_print(traceback.format_exc())
                    messages.error(request, UTL.error_message('DB_EX_ER'))

            elif request.GET['search_option'] == 'patient_blood_group' and request.GET.get(
                'patient_name_or_blood_group') != '':
                filters = [Q(patient__hospital=request.hospital),
                           Q(patient__blood_group__icontains=request.GET.get('patient_name_or_blood_group')),
                           UTL.address_filter_query(request.GET.get('country'), request.GET.get('region'),
                                                    request.GET.get('district'), request.GET.get('town'),
                                                    request.GET.get('postcode'))]
                try:
                    query_by_blood = Patient.objects.filter(patient__status='active', hospital=request.hospital,
                                                            *filters).distinct()
                    message = f"Town: {request.GET.get('town', '')}, Postcode: {request.GET.get('postcode', '')}, " \
                              f"Patient blood group: {request.GET.get('patient_name_or_blood_group')}. Check other " \
                              f"columns for more detail. "

                    create_activity(request, 'GET', message, check_activity_level(request))
                    patients = UTL.fetch_sorted_query(query_by_blood, request.GET.get('sort'), 'created')
                    paginator = UTL.view_pagination(patients, request.GET.get('page', 1), 30)
                    page_obj = paginator.get('page_obj')

                    if paginator.get('count', 0) > 0:
                        messages.success(request, UTL.success_message('ADVANCED_SEARCH'))
                    else:
                        messages.success(request, UTL.success_message('ADVANCED_SEARCH_NOT'))
                except Exception as e:
                    messages.error(request, UTL.error_message('DB_EX_ER'))

    context = {
        'title': 'Advanced Search | Patients',
        'page_obj': page_obj,
        'regions': Region.objects.filter(status='active'),
        'districts': District.objects.filter(status='active'),
        'towns': Town.objects.filter(status='active'),
        'postcodes': Postcode.objects.filter(status='active'),
    }

    return render(request, 'patients/patient_advanced_search_list.html', context)


@login_required
@logged_in_user(['hospital level', 'practitioner level'])
@fetch_user_details
@check_token(['practitioner level'])
def patient_search_by_keyword(request):
    page_obj = None
    search_word = request.GET.get('keyword')
    if request.method == 'GET' and 'keyword' in request.GET:
        if not search_word:
            return redirect(reverse("patients:keyword"))
        else:
            try:
                keyword = get_object_or_404(Keyword, pk=search_word)
                query = Patient.objects.filter(
                    status='active',
                    hospital=request.hospital,
                    medical_session_patient__keywords=keyword
                ).prefetch_related(
                    Prefetch('patient_image', PatientImage.objects.filter(status='active', current_image=True), "current_photo")
                ).distinct()

                patients = UTL.fetch_sorted_query(query, request.GET.get('sort'), 'created')
                paginator = UTL.view_pagination(patients, request.GET.get('page', 1), 30)
                page_obj = paginator.get('page_obj')

                message = _(
                    'Patient record is searched(keyword) with %(w)s. Check other columns for more detail.'
                ) % {'w': search_word}

                create_activity(request, 'GET', message, check_activity_level(request))
                if paginator.get('count', 0) > 0:
                    messages.success(request, UTL.success_message('ADVANCED_SEARCH'))
                else:
                    messages.success(request, UTL.success_message('ADVANCED_SEARCH_NOT'))
            except:
                messages.error(request, UTL.error_message('DB_EX_ER'))

    context = {
        'searched': search_word,
        'title': 'Patients Keyword Search',
        'keywords': Keyword.objects.filter(status='active'),
        'page_obj': page_obj,
    }

    return render(request, "patients/patient_keyword_search_list.html", context)


@login_required
@logged_in_user(['practitioner level'])
@fetch_user_details
@check_token(['practitioner level'])
def patient_death_record(request, pk):
    try:
        patient = Patient.objects.get(pk=pk, status='active', vital_status=False)
    except Patient.DoesNotExist:
        messages.error(request, _('Something went wrong. Please check your records or contact us to update vital '
                                  'status of patient.'))
        return redirect(reverse('patients:detail', args=(pk,)))

    create_activity(
        request,
        'GET',
        _('Patient death record form is visited.'),
        check_activity_level(request)
    )

    if patient.hospital is not request.hospital:
        messages.error(request, _('Patient is not in your hospital.'))
        return redirect(reverse('patients:detail', args=(pk,)))

    if request.method == 'POST':
        form = PatientDeathRecordForm(request.POST or None)

        if form.is_valid():
            try:
                with transaction.atomic():
                    x = form.save(commit=False)
                    x.patient = patient
                    x.practitioner = request.user
                    x.hospital = request.hospital
                    x.creator_user = request.user
                    x.save()

                    create_activity(
                        request,
                        'INSERT',
                        _('Patient death record id created.'),
                        check_activity_level(request),
                        patient
                    )
                messages.success(request, _('Patient body is released from mortuary.'))
                return redirect(reverse('mortuaries:list', args=(pk,)))
            except DatabaseError:
                messages.error(request, _('Something went wrong. Try again.'))
                create_activity(
                    request,
                    'INSERT ERROR',
                    _('Patient death record creation is failed.'),
                    check_activity_level(request),
                    patient
                )
                return redirect(reverse('patients:detail', args=(pk,)))
    else:
        form = PatientDeathRecordForm()

    data_send = {
        'title': 'Death Record | Patient',
        'patient': patient,
        'form': form,
    }

    return render(request, "patients/create_patient_death_record.html", data_send)
