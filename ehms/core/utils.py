import random
import uuid

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

verhoeff_table_d = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
    (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
    (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
    (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
    (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
    (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
    (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
    (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
    (9, 8, 7, 6, 5, 4, 3, 2, 1, 0)
)
verhoeff_table_p = (
    (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
    (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
    (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
    (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
    (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
    (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
    (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
    (7, 0, 4, 6, 9, 1, 3, 2, 5, 8)
)

verhoeff_table_inv = (0, 4, 3, 2, 1, 5, 6, 7, 8, 9)


def calc_sum(number):
    """For a given number returns a Verhoeff checksum digit"""
    c = 0
    for i, item in enumerate(reversed(str(number))):
        c = verhoeff_table_d[c][verhoeff_table_p[(i + 1) % 8][int(item)]]
    return verhoeff_table_inv[c]


def generate_verhoeff(number):
    """For a given number returns number + Verhoeff checksum digit"""
    return "%s%s" % (number, calc_sum(number))


def verhoeff_random_number(count, length):
    i = 0
    final_random_number = ''

    if length == 6:
        random_number = str(random.randint(11, 99)) + \
                        str(random.randint(11, 99)) + \
                        str(random.randint(1, 9))
    elif length == 8:
        random_number = str(random.randint(111, 999)) + \
                        str(random.randint(11, 99)) + \
                        str(random.randint(11, 99))
    elif length == 10:
        random_number = str(random.randint(1111, 9999)) + \
                        str(random.randint(111, 999)) + \
                        str(random.randint(11, 99))
    elif length == 12:
        random_number = str(random.randint(1111, 9999)) + \
                        str(random.randint(1111, 9999)) + \
                        str(random.randint(111, 999))
    elif length == 16:
        random_number = str(random.randint(1111, 9999)) + \
                        str(random.randint(1111, 9999)) + \
                        str(random.randint(1111, 9999)) + \
                        str(random.randint(111, 999))
    elif length == 20:
        random_number = str(random.randint(1111, 9999)) + \
                        str(random.randint(11111, 99999)) + \
                        str(random.randint(11111, 99999)) + \
                        str(random.randint(11111, 99999))
    else:
        random_number = str(random.randint(111111, 999999))

    while i < count:
        # Add verhoeff checksum
        verhoeff_checksum_added_number = generate_verhoeff(random_number)

        # convert checksum added number into string
        check = str(type(verhoeff_checksum_added_number))

        while check == "<class 'NoneType'>":
            # again added verhoeff checksum
            verhoeff_checksum_added_number = generate_verhoeff(random_number)
            # again convert checksum added number into string
            check = str(type(verhoeff_checksum_added_number))
        final_random_number += verhoeff_checksum_added_number
        i += 1

    return final_random_number


def string_to_dash(str):
    for i in range(0, len(str), 1):
        if str[i] == ' ':
            str = str.replace(str[i], '-')
    return str


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def kurrent_timestamp():
    return parse_datetime(timezone.localtime(timezone.now()).strftime('%Y-%m-%d %H:%M:%S')).timestamp()


def check_activity_level(request):
    activity_tag = None
    if request.group_name == 'hospital level':
        activity_tag = 'Hospital'
    elif request.group_name == 'nurse level':
        activity_tag = 'Nurse'
    elif request.group_name == 'practitioner level':
        activity_tag = 'Practitioner'
    elif request.group_name == 'inventory level':
        activity_tag = 'Inventory'
    elif request.group_name == 'mortuary level':
        activity_tag = 'Mortuary'
    elif request.group_name == 'region level':
        activity_tag = 'Region'
    elif request.group_name == 'reception level':
        activity_tag = 'Reception'
    elif request.group_name == 'country level':
        activity_tag = 'Country'
    elif request.group_name == 'district level':
        activity_tag = 'District'

    return activity_tag


STATUS = Choices(_('active'), 'inactive')

BLOOD_GROUP_CHOICES = Choices(
    _('A Positive'),
    _('O Positive'),
    _('B Positive'),
    _('AB Positive'),
    _('A Negative'),
    _('O Negative'),
    _('B Negative'),
    _('AB Negative'),
)
PREGNANCY_CHOICES = Choices(
    _('Pregnant'),
    _('Not Pregnant'),
    _('Not Applicable'),
)
MARITAL_CHOICES = Choices(
    _('Married'),
    _('Unmarried'),
    _('Divorced'),
    _('Widow'),
    _('Widower'),
)
RELIGION_CHOICES = Choices(
    _('Islam'),
    _('Christianity'),
    _('Baha i Faith'),
    _('African Traditional Faith'),
    _('Hinduism'),
    _('Buddhism'),
    _('Folk religions'),
    _('Sikhism'),
    _('Judaism'),
    _('Others'),
    _('No Religion'),
)
GENDER_CHOICES = Choices(
    _('Male'),
    _('Female'),
    _('Transgender'),
)
ADDRESS_CHOICES = Choices(
    _('Temporary'),
    _('Permanent'),
)
RESPONSE_CHOICE = Choices(
    _('Pending'),
    _('In process'),
    _('Rejected'),
    _('Completed'),
)
ARTICLE_TYPE = Choices(
    _('Article Sticky Big'),
    _('Article Sticky Aside'),
    _('Article Other'),
)
RELATIONS = Choices(
    _('Great Grand Father'),
    _('Grand Father'),
    _('Father'),
    _('Step-Father'),
    _('Great Grand Mother'),
    _('Grand Mother'),
    _('Mother'),
    _('Step-Mother'),
    _('Daughter'),
    _('Son'),
    _('Wife'),
    _('Husband'),
    _('Child'),
    _('Brother'),
    _('Sister'),
    _('Grand Son'),
    _('Grand Daughter'),
    _('Step-Child'),
    _('Adopted Child'),
    _('Mother-in-law'),
    _('Father-in-law'),
    _('Daughter-in-law'),
    _('Brother-in-law'),
    _('Sister-in-law'),
    _('Uncle'),
    _('Aunt'),
    _('Nephew'),
    _('Niece'),
    _('Other'),

)
PULSE_CHOICES = Choices(
    0, 180, 170, 160, 150, 140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40
)
TEMPERATURE_CHOICES = Choices(
    105, 104, 103, 102, 101, 100, 99, 98.6, 98, 97, 96, 95
)
INVENTORY_STOCK_TYPE = Choices(
    _('Stock In'),
    _('Stock Out'),
)

