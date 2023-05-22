import traceback

from django.db import DatabaseError
from django.utils.translation import gettext_lazy as _

from ehms.activities.models import Activity
from ipware import get_client_ip


def cam():
    return {
        'new_patient': _('New patient is registered.'),
        'activity_page':  _('Activity page is fetched.'),
        'hospital_ms_page': _('Hospital Medical Sessions is fetched.'),
        'reception_list_page': _('Reception list page is fetched.'),
        'reception_level_dashboard_1': _('The user has accessed the reception dashboard page.'),
        'reception_level_dashboard_2': _('The token has been successfully verified by the user.'),
        'hospital_query_inbox': _('A hospital query has been created. Please refer to other columns for further '
                                  'details.')
    }


def create_activity(request, action, message=None, activity_level=None, patient=None):
    client_ip, is_routable = get_client_ip(request)

    try:
        user = request.user
    except:
        user = None

    try:
        hospital = request.hospital
    except:
        hospital = None

    try:
        user_agent = request.headers.get('user_agent')
    except:
        user_agent = None

    try:
        group_name = request.group_name
    except:
        group_name = None

    try:
        client_ip = client_ip
    except:
        client_ip = None

    try:
        is_routable = is_routable
    except:
        is_routable = None

    try:
        user_unique_id = request.user.user_unique_id
    except:
        user_unique_id = None

    try:
        Activity.objects.create(
            creator_user=user,
            action=action,
            activity_level=activity_level,
            patient=patient,
            hospital=hospital,
            description=message,
            user_agent=user_agent,
            user_group=group_name,
            ip_address=client_ip,
            ip_routable=is_routable,
            uid=user_unique_id,
        )
    except DatabaseError:
        pass


