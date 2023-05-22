from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import localtime

from ehms.addresses.models import Country, Region, District
from ehms.core.utils import string_to_dash
from ehms.hospitals.models import Hospital
from ehms.nurses.models import NurseHospital, Nurse
from ehms.practitioners.models import PractitionerHospital, Practitioner
from ehms.receptions.models import Reception
from ehms.utils.helpers import UTL


def is_not_staff(user):
    return not user.is_staff


def home_visit(view_function):
    """
    Home visit is decorator to redirect user to their specific home page after logged in
    """

    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated and is_not_staff(request.user) and len(request.user.groups.all()) > 0:
            group = request.user.groups.all()[0].name
            request.yahoooo = True
            group_link = '/dashboards/' + string_to_dash(group) + '/'
            return redirect(group_link)
        elif request.user.is_authenticated and request.user.is_staff:
            return redirect(reverse('admin:index'))
        else:
            request.yahoooo = False
            return view_function(request, *args, **kwargs)

    return wrapper_function


def logged_in_user(level):
    """
    Check if user is logged in with specific group name which is called as level
    """

    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            # TODO: improve session expiry and shift it in middleware on each request
            # check if session time is still available or not for the user
            # if not localtime(request.user.login_session_timestamp) > timezone.now():
            #     logout(request)
            #     messages.info(request, 'Your session is expired. Try to login again.')
            #     return redirect(reverse('login'))
            # fetch the group name
            if request.user.groups.exists() and len(request.user.groups.all()) > 0:
                request.group_name = request.user.groups.all()[0].name
                request.yahoooo = True
                if request.group_name not in level:
                    return redirect('404.html')
            else:
                logout(request)  # Todo: See if this is necessary or simply use login redirect
                messages.info(request, 'Something went wrong. Try to login again.')
                return redirect(reverse('login'))
            return view_function(request, *args, **kwargs)

        return wrapper

    return decorator


def fetch_user_details(view_function):
    """
    fetch the hospital/practitioner/nurse/mortuary/inventory/reception/other dashboards with their hospital
    """

    def wrapper_function(request, *args, **kwargs):
        if request.group_name != '' and request.user.userprofile.user_unique_id != '':
            user_unique_id = request.user.userprofile.user_unique_id
            if request.group_name == 'hospital level':
                request.hospital = get_object_or_404(Hospital, uid=user_unique_id, status='active')
            elif request.group_name == 'practitioner level':
                request.practitioner = get_object_or_404(Practitioner, status='active', uid=user_unique_id)
                # ch= current hospital TODO check practitioner_ch_record what it contains
                practitioner_ch_record = get_object_or_404(PractitionerHospital, status='active', current_hospital=True,
                                                           practitioner=request.practitioner.pk)
                request.hospital = get_object_or_404(Hospital, status='active', pk=practitioner_ch_record.hospital.pk)
                if (
                    request.practitioner.verify_token is False or
                    localtime(request.practitioner.token_timestamp) < timezone.now()
                ):
                    request.client_token_check = 'failed'
                else:
                    request.client_token_check = 'passed'

            elif request.group_name == 'nurse level':
                request.nurse = get_object_or_404(Nurse, status='active', uid=user_unique_id)
                # ch = current hospital TODO Check nurse_ch_record what it contains
                nurse_ch_record = get_object_or_404(NurseHospital, status='active', current_hospital=True,
                                                    nurse=request.nurse.pk)
                request.hospital = get_object_or_404(Hospital, status='active', pk=nurse_ch_record.hospital.pk)
                if (
                    request.nurse.verify_token is False or
                    localtime(request.nurse.token_timestamp) < timezone.now()
                ):
                    request.client_token_check = 'failed'
                else:
                    request.client_token_check = 'passed'
            elif request.group_name == 'mortuary level':
                pass
                # request.hospital = get_object_or_404(Hospital, uid=user_unique_id, status='active')
            elif request.group_name == 'inventory level':
                pass
                # request.hospital = get_object_or_404(Hospital, uid=user_unique_id, status='active')
            elif request.group_name == 'reception level':
                request.reception = get_object_or_404(Reception, status='active', uid=user_unique_id)
                # TODO: fetch hospital in one query
                request.hospital = get_object_or_404(Hospital, pk=request.reception.hospital.pk, status='active')

                if (
                    request.reception.verify_token is False or
                    localtime(request.reception.token_timestamp) < timezone.now()
                ):
                    request.client_token_check = 'failed'
                else:
                    request.client_token_check = 'passed'

            elif request.group_name == 'country level':
                request.country = get_object_or_404(Country, status='active', uid=user_unique_id)
            elif request.group_name == 'region level':
                request.region = get_object_or_404(Region, status='active', uid=user_unique_id)
                request.country = request.region.country
            elif request.group_name == 'district level':
                request.district = get_object_or_404(District, status='active', uid=user_unique_id)
                request.country = request.district.country
                request.region = request.district.region
            else:
                return redirect('404.html')  # TODO: see if this is okay! or we should logout user here?
        else:
            return redirect(reverse('login'))
        return view_function(request, *args, **kwargs)

    return wrapper_function


def check_token(level):
    """
    Check token for employees within the hospital
    """

    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            # Check point (I) : - The group name must be one of the allowed levels array or list
            if request.group_name in level:
                # Check point (II) : -
                # 1. Conditions for each level to verify token
                # 2. Check for existence of token
                # 3. Check for token timestamp is expired or not
                if (
                    request.group_name == 'practitioner level' and
                    (
                        request.practitioner.verify_token is False or
                        localtime(request.practitioner.token_timestamp) < timezone.now()
                    )
                ):
                    request.client_token_check = 'failed'
                    messages.error(request, _('Token is not generated or expired.'))
                    return redirect('/dashboards/practitioner-level/')  # TODO: replace with reverse
                elif (
                    request.group_name == 'nurse level' and
                    (
                        request.nurse.verify_token is False or
                        localtime(request.nurse.token_timestamp) < timezone.now()
                    )
                ):
                    request.client_token_check = 'failed'
                    messages.error(request, _('Token is not generated or expired.'))
                    return redirect('/dashboards/nurse-level/')  # TODO: replace with reverse
                elif (
                    request.group_name == 'reception level' and
                    (
                        request.reception.verify_token is False or
                        localtime(request.reception.token_timestamp) < timezone.now()
                    )
                ):
                    request.client_token_check = 'failed'
                    messages.error(request, _('Token is not generated or expired.'))
                    return redirect('/dashboards/reception-level/')  # TODO: replace with reverse
                else:
                    request.client_token_check = 'passed'
                    return view_function(request, *args, **kwargs)
            else:
                return view_function(request, *args, **kwargs)
            # TODO this code needs to be improve
        return wrapper

    return decorator
