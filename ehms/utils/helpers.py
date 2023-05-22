import calendar
import datetime
import os
import random
import re
import uuid

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from model_utils import Choices


class CC:

    def __init__(self):
        pass

    IPD_MEDICAL_SESSION_STATUS = Choices(
        _('Discharged'),
        _('Occupied'),
        _('Not Applicable')
    )

    DEPARTMENT_CHOICES = Choices(
        _('OPD'),
        _('IPD'),
    )
    GENDER_CHOICES = Choices(
        _('Male'),
        _('Female'),
        _('Transgender'),
    )

    BOOL = Choices(
        (_('Yes'), True),
        (_('No'), False),
    )

    MEDICATION_STATUS = Choices(
        _('Given'),
        _('Refused'),
        _('Destroyed'),
        _('Nausea'),
        _('Vomiting'),
        _('Hospital'),
        _('On Leave'),
        _('Discontinued'),
        _('Other reason'),
    )

    COUNTRY_CHOICES = Choices(
        _('United Kingdom'),
    )

    STATUS_CHOICES = Choices(
        _('active'),
        _('inactive'),
    )

    DAYS = Choices(
        _('Sunday'),
        _('Monday'),
        _('Tuesday'),
        _('Wednesday'),
        _('Thursday'),
        _('Friday'),
        _('Saturday')
    )

    ADDRESS_CHOICES = Choices(
        _('Temporary'),
        _('Permanent')
    )

    ROTA_CHOICES = Choices(
        'Flexible',
        'Inflexible'
    )

    TASK_STATUS = Choices(
        'Created',
        'In Progress',
        'Cancelled',
        'Finished',
        'Missed',
        'Not Completed',
        'Delayed',
    )

    VIEW_CHOICES = Choices(
        'Calendar View',
        'List View',
    )

    SHIFTS = Choices(
        'Morning',
        'Breakfast',
        'Lunch',
        'Afternoon',
        'Tea',
        'Evening',
        'Dinner',
        'Night',
    )


class UTL:

    def __init__(self):
        pass

    @staticmethod
    def error_message(key):
        d = {
            # Database exception error
            "DB_EX_ER": _("An error occurred. Please try again or contact us if the issue persists."),
            "TOKEN_NOT_VERIFIED": _("An error occurred. Please verify if the token has expired or not."),
            "BOTH_DATES_REQUIRED": _("Please provide both dates."),
        }
        return d.get(key)

    @staticmethod
    def success_message(key):
        d = {
            "PATIENT_REGISTER": _("New patient registered successfully."),
            "TOKEN_VERIFIED": _("The token has been successfully verified."),
            "INBOX_QUERY_SUBMIT": _("Thank you for your query. We'll respond shortly."),
            "ADVANCED_SEARCH": _("Success: Search Results Found"),
            "ADVANCED_SEARCH_NOT": _("Success: Search Results Not Found"),
            "HOSPITAL_RANGE_DASHBOARD": _("Query executed successfully."),
        }
        return d.get(key)

    @staticmethod
    def qr_upload_setup(instance, filename):
        now = timezone.now()
        base, extension = os.path.splitext(filename)
        extension = extension.lower()
        o = ContentType.objects.get_for_model(instance)
        return f'{o.app_label}/images/{now:%Y/%m}/qr-{base}{extension}'

    @staticmethod
    def image_upload_setup(instance, filename):
        now = timezone.now()
        base, extension = os.path.splitext(filename)
        extension = extension.lower()
        o = ContentType.objects.get_for_model(instance)
        return f'{o.app_label}/images/{now:%Y/%m}/cms-{instance.pk}{extension}'

    @staticmethod
    def document_upload_setup(instance, filename):
        now = timezone.now()
        base, extension = os.path.splitext(filename)
        extension = extension.lower()
        o = ContentType.objects.get_for_model(instance)
        return f'{o.app_label}/documents/{now:%Y/%m}/cms-{instance.pk}{extension}'

    @staticmethod
    def check_string_valid_date(d: str):
        """

        Check if the string is a valid date or not
        if found valid return the date

        @param d: string which you want to validate as datetime (Format Y-m-d)
        @type d: str
        @return: It will return boolean value False or 'datetime.date' as per the string you supplied
        @rtype: bool | datetime
        """

        if not isinstance(d, str):
            return False

        try:
            return timezone.make_aware(timezone.datetime.strptime(d, '%Y-%m-%d')).date()
        except ValueError:
            return False

    @staticmethod
    def check_string_valid_datetime(d: str):
        """

        Check if the string is a valid datetime or not
        if found valid return the datetime with timezone using make_aware

        @param d: string which you want to validate as datetime (Format Y-m-d H:M:S)
        @type d: str
        @return: It will return boolean value False or 'datetime.datetime' as per the string you supplied
        @rtype: bool | datetime.datetime
        """

        if not isinstance(d, str):
            return False

        try:
            return timezone.make_aware(timezone.datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))
        except ValueError:
            return False

    @staticmethod
    def check_valid_date(d: object):
        """

        Check if the object is a valid date or not
        if found valid return the date

        @param d: object which you want to validate as datetime
        @type d: object
        @return: It will return boolean value False or 'datetime.date' as per the object you supplied
        @rtype: bool | datetime
        """

        if not isinstance(d, datetime.date):
            return False

        d = f'{str(d.year)}-{str(d.month)}-{str(d.day)}'

        try:
            return timezone.make_aware(timezone.datetime.strptime(d, '%Y-%m-%d')).date()
        except ValueError:
            return False

    @staticmethod
    def check_valid_datetime(d: object):
        """

        Check if the object is a valid datetime or not;
        if found valid return the timezone datetime using make_aware method

        @param d: object which you want to validate as datetime.datetime
        @type d: object
        @return: It will return boolean value False or 'datetime.datetime' as per the datetime object you supplied
        @rtype: bool | datetime.datetime
        """

        if not isinstance(d, datetime.datetime):
            return False

        d = f'{str(d.year)}-{str(d.month)}-{str(d.day)} {str(d.hour)}:{str(d.minute)}:{str(d.second)}'

        try:
            return timezone.make_aware(datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S'))
        except ValueError:
            return False

    @staticmethod
    def string_to_dash(i: str):
        """

        Convert string spaces into dashes

        @param i: String which contains spaces, and you want to replace it with dashes
        @type i: str
        @return: String where spaces are replaced with dashes
        @rtype: str
        """

        if not isinstance(i, str):
            return i

        i = i.strip()

        for x in range(0, len(i), 1):
            if i[x] == ' ':
                i = i.replace(i[x], '-')
        return i

    @staticmethod
    def calculate_age(bd: str | datetime.date):
        """

        Get age from date of birth

        @param bd: It can be date string or date object
        @type bd: str | date
        @return: Calculate age from the date of birth and returns
        @rtype: int
        """

        if isinstance(bd, str):
            try:
                return int((timezone.now().date() - timezone.datetime.strptime(bd, '%Y-%m-%d').date()).days / 365.2425)
            except ValueError:
                return None
        elif isinstance(bd, datetime.date):
            bd = f'{str(bd.year)}-{str(bd.month)}-{str(bd.day)}'
            try:
                return int(
                    (
                        timezone.now().date() - timezone.make_aware(timezone.datetime.strptime(bd, '%Y-%m-%d')).date()
                    ).days / 365.2425
                )
            except ValueError:
                return None
        else:
            return None

    @staticmethod
    def is_valid_uuid(val: str):
        """

        Verify if uuid is a valid uuid string or not

        @param val: any string which you want to verify as uuid
        @type val: str
        @return: True or False
        @rtype: bool
        """
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    @staticmethod
    def get_day(day: int):
        return ({
            0: 'Monday',
            1: 'Tuesday',
            2: 'Wednesday',
            3: 'Thursday',
            4: 'Friday',
            5: 'Saturday',
            6: 'Sunday',
        }).get(day, None)

    @staticmethod
    def file_validation(
        file: str,
        allowed_formats: list,
        allowed_mime_types: list,
        allowed_upload_size: int,
        allowed_width: list,
        allowed_height: list,
        file_type: str,
        field_name: str,
        image_dim: str = 'free',
        file_placeholder: str = 'file'
    ):

        """

        The file validation method

        @param file: The file itself
        @type file: str
        @param allowed_formats: ['jpg', 'jpeg', 'png', 'pdf' ...]
        @type allowed_formats: dict
        @param allowed_mime_types: ['image/jpeg', 'application/msword', 'application/vnd.ms-excel' ...]
        @type allowed_mime_types: int
        @param allowed_upload_size: 2, 5, 10 =>  The Size is in Megabytes
        @type allowed_upload_size: dict
        @param allowed_width: [300, 600] ... => It is a range in pixels.
        @type allowed_width: dict
        @param allowed_height: [200, 500] ... => It is a range in pixels.
        @type allowed_height: dict
        @param file_type: 'image', 'pdf', 'doc' ...
        @type file_type: These are the allowed file types for now => image, pdf, doc, sheet
        @param field_name: str
        @type field_name: The field name 'from the form' against which you want to display the message.
        @param image_dim: Image dimension can be 'square' or 'free'.
        @type image_dim: str
        @param file_placeholder:  The size of "passport" is invalid. here the passport is the placeholder.
        @type file_placeholder: str
        @return: None but raise the validation errors
        @rtype: None
        @raise ValidationError:
            The list of validation errors are as follows.
                1. image:
                    - extension check error
                    - mime type check error
                    - size validation error
                    - dimension validation error
                2. pdf:
        """

        if file_type == 'image':
            from PIL import Image
            image_file = Image.open(file)

            # Extension validation
            if image_file.format not in allowed_formats:
                raise ValidationError({
                    str(field_name): [
                        _('The %s is invalid. Only %s format files are allowed.') %
                        (file_placeholder, ', '.join(allowed_formats),)
                    ]
                })

            # MIME Type validation
            if image_file.get_format_mimetype() not in allowed_mime_types:
                raise ValidationError({
                    str(field_name): [
                        _('The %s is invalid. Only %s mime-type files are allowed.') %
                        (file_placeholder, ', '.join(allowed_formats),)
                    ]
                })

            # Size validation
            filesize = int(len(image_file.fp.read()))
            filesize_limit = allowed_upload_size

            if filesize > int(filesize_limit * 1024 * 1024):
                raise ValidationError({
                    str(field_name): [_('Max %s size is %sMB') % (file_placeholder, filesize_limit,)]
                })

            # Dimension validation
            # get the upload image size
            w, h = image_file.size

            # allowed width is a dict with range of width
            # the first element of the dict (allowed width and allowed height)
            # is smallest in range and the second is largest in range.
            # i.e. [200, 400] the image should be inbetween 200 and 400 pixels wide

            # check if allowed width dict has only one element i.e. there is no range required
            # if it is one element then simply compare it with measured width i.e. w
            if len(allowed_width) == 1 and allowed_width[0] != w:
                raise ValidationError({
                    str(field_name): [
                        _('The %s is %s pixel wide. It should be %s pixel wide.') %
                        (file_placeholder, w, allowed_width[0])
                    ]
                })
            # here the allowed width is a range as both the elements are required
            # compare it against the measured width i.e. w
            elif len(allowed_width) == 2 and (w <= allowed_width[0] or w >= allowed_width[1]):
                raise ValidationError({
                    str(field_name): [
                        _('The %s is %s pixel wide. It should be in between %s - %s pixel wide.') %
                        (file_placeholder, w, allowed_width[0], allowed_width[1])
                    ]
                })
            # now comes the height
            # if allowed height which is a dict got one element
            # then chances are image might have some fixed ratio requirements i.e. 200 x 200
            # in that scenario the image_dim is going to be checked alongside the allowed height
            # if image_dim = free ( by default)
            # this means image's measured height is going to check just with the allowed height
            elif len(allowed_height) == 1 and image_dim == 'free' and allowed_height[0] != h:
                raise ValidationError({
                    str(field_name): [
                        _('The %s is %s pixel high. It should be %s pixel high.') %
                        (file_placeholder, w, allowed_height[0])
                    ]
                })
            # if image_dim = square (another option available)
            # then this means we have to check allowed height with measured width of the image instead height
            # rest the single element in the allowed height dict is also going to check
            elif len(allowed_height) == 1 and image_dim == 'square' and allowed_height[0] != w:
                raise ValidationError({
                    str(field_name): [
                        _('The %s is %s pixel high. It should be %s pixel high.') % (file_placeholder, h, w,)
                    ]
                })
            # if allowed height dict has 2 elements then it is a range i.e. [150, 180]
            # image_dim = free scenario is the same
            elif len(allowed_height) == 2 and \
                image_dim == 'free' and \
                (h <= allowed_height[0] or h >= allowed_height[1]):
                raise ValidationError({
                    str(field_name): [
                        _('The %s is %s pixel high. It should be in between %s - %s pixel high.') %
                        (file_placeholder, w, allowed_height[0], allowed_height[1],)
                    ]
                })
            # image_dim = square scenario is the same
            elif len(allowed_height) == 2 and \
                image_dim == 'square' and \
                (h <= allowed_height[0] or h >= allowed_height[1] or h != w):
                raise ValidationError({
                    str(field_name): [
                        _('The %s is %s pixel high. It should be in between'
                          ' %s - %s pixel high and equals to %s pixel.') %
                        (file_placeholder, h, allowed_height[0], allowed_height[1], w)
                    ]
                })
        elif file_type == 'pdf':
            pass  # TODO

    @staticmethod
    def check_tz_aware(d: datetime.datetime):
        """

        Debug function: Check if datetime is timezone aware or not

        @param d: Datetime object
        @type d: datetime.datetime
        @return: None but Just print AWARE or UNAWARE along with datetime
        @rtype: None
        """

        if not isinstance(d, datetime.datetime):
            print('--------------------------------------------------------------------')
            print('It is not a valid datetime.datetime object. Feed something pure.')
            print('--------------------------------------------------------------------')
        else:
            try:
                t = timezone.is_aware(d)

                if t is None:
                    print('[[[[[[[[[[[[[[[[[[[[[[[ UNAWARE ]]]]]]]]]]]]]]]]]]]]]]]')
                    print(d)
                else:
                    print('[[[[[[[[[[[[[[[[[[[[[[[[[ AWARE ]]]]]]]]]]]]]]]]]]]]]]]]]')
                    print(d)
            except AttributeError:
                print('[[[[[[[[[[[[[[[[[[[[[[[ UNAWARE ]]]]]]]]]]]]]]]]]]]]]]]')
                print(d)

    @staticmethod
    def mobile_check(request):
        """
        Return True if the request comes from a mobile device.
        """

        mobile_agent = re.compile(r".*(iphone|mobile|androidtouch)", re.IGNORECASE)

        if mobile_agent.match(request.META['HTTP_USER_AGENT']):
            return True
        else:
            return False

    @staticmethod
    def fetch_sorted_query(query, sort_by, field):
        print(query)
        if sort_by not in ['asc', 'desc']:
            sort_by = 'desc'

        if sort_by == 'asc':
            return query.order_by(f"{field}")
        elif sort_by == 'desc':
            return query.order_by(f"-{field}")

    @staticmethod
    def fetch_sort_basic(sort_by, field):
        if sort_by not in ['asc', 'desc']:
            sort_by = 'desc'

        if sort_by == 'asc':
            return f"{field}"
        elif sort_by == 'desc':
            return f"-{field}"

    @staticmethod
    def view_pagination(clients, page, items):
        is_paginated = False
        from django.core.paginator import Paginator
        paginator = Paginator(clients, items)
        page_number = page
        page_obj = paginator.get_page(page_number)

        if paginator.count > items:
            is_paginated = True

        return {
            'page_obj': page_obj,
            'is_paginated': is_paginated,
            'count': paginator.count
        }

    @staticmethod
    def custom_print(output):
        random_string = [
            '---------------------------------------------------------------------------------------------------------',
            '_________________________________________________________________________________________________________',
            '=========================================================================================================',
            '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++',
            '/////////////////////////////////////////////////////////////////////////////////////////////////////////',
            '+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+',
            '.........................................................................................................',
            ',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,',
            '#########################################################################################################',
        ]

        line_string = random_string[random.randint(0, 8)]

        print(line_string)
        print(output)
        print(line_string)

    @staticmethod
    def name_filter_query(name_string):
        names = name_string.split()
        first_name = names[0]
        last_name = names[-1] if len(names) > 1 else ''
        middle_name = " ".join(names[1:-1])

        filters = []
        if first_name:
            filters.append(Q(first_name__icontains=first_name))
        if middle_name:
            filters.append(Q(middle_name__icontains=middle_name))
        if last_name:
            filters.append(Q(last_name__icontains=last_name))
        return filters

    @staticmethod
    def address_filter_query(country=None, region=None, district=None, town=None, postcode=None):
        filters = []
        if country:
            filters.append(Q(patient_belong_to_address__country_id=country))
        if region:
            filters.append(Q(patient_belong_to_address__region_id=region))
        if district:
            filters.append(Q(patient_belong_to_address__district_id=district))
        if town:
            filters.append(Q(patient_belong_to_address__town_id=town))
        if postcode:
            filters.append(Q(patient_belong_to_address__postcode_id=postcode))
        return filters


class RandomDigits:
    count = 1
    length = 10
    final_random_number = ''
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

    def __init__(self, count, length):

        if isinstance(count, int) and 0 < count < 5:
            self.count = count
        if isinstance(length, int) and 0 < length < 500:
            self.length = length
        self.verhoeff_random_number()

    @staticmethod
    def get(count, length):
        x = RandomDigits(count, length)
        return x.final_random_number

    def calc_sum(self, number: int):
        """

        @param number: Given integer number
        @type number: int
        @return: returns a Verhoeff checksum digit
        @rtype: int
        """
        c = 0
        for i, item in enumerate(reversed(str(number))):
            c = self.verhoeff_table_d[c][self.verhoeff_table_p[(i + 1) % 8][int(item)]]
        return self.verhoeff_table_inv[c]

    def generate_verhoeff(self, number: int):
        """

        @param number: Any random number
        @type number: int
        @return: For a given number returns number + Verhoeff checksum digit
        @rtype: str
        """
        return "%s%s" % (number, self.calc_sum(number))

    @staticmethod
    def similar_digit_pattern(length, string_pattern):
        i = 1
        pattern = ''
        while i < length:
            pattern += string_pattern
            i += 1
        return int(pattern)

    def verhoeff_random_number(self):
        """
        Generate the final number
        """
        i = 0

        if self.length == 6:
            random_number = str(random.randint(11, 99)) + \
                            str(random.randint(11, 99)) + \
                            str(random.randint(1, 9))
        elif self.length == 8:
            random_number = str(random.randint(111, 999)) + \
                            str(random.randint(11, 99)) + \
                            str(random.randint(11, 99))
        elif self.length == 10:
            random_number = str(random.randint(1111, 9999)) + \
                            str(random.randint(111, 999)) + \
                            str(random.randint(11, 99))
        elif self.length == 12:
            random_number = str(random.randint(1111, 9999)) + \
                            str(random.randint(1111, 9999)) + \
                            str(random.randint(111, 999))
        elif self.length == 16:
            random_number = str(random.randint(1111, 9999)) + \
                            str(random.randint(1111, 9999)) + \
                            str(random.randint(1111, 9999)) + \
                            str(random.randint(111, 999))
        elif self.length == 20:
            random_number = str(random.randint(1111, 9999)) + \
                            str(random.randint(11111, 99999)) + \
                            str(random.randint(11111, 99999)) + \
                            str(random.randint(11111, 99999))
        else:
            random_number = str(random.randint(
                self.similar_digit_pattern(self.length, '1'), self.similar_digit_pattern(self.length, '9')
            ))

        while i < self.count:
            # Add verhoeff checksum
            verhoeff_checksum_added_number = self.generate_verhoeff(int(random_number))

            # convert checksum added number into string
            check = type(verhoeff_checksum_added_number)

            while check == "<class 'NoneType'>":
                # again added verhoeff checksum
                verhoeff_checksum_added_number = self.generate_verhoeff(int(random_number))
                # again convert checksum added number into string
                check = type(verhoeff_checksum_added_number)
            self.final_random_number += verhoeff_checksum_added_number
            i += 1

        return self.final_random_number


class NavigateCalendar:
    """
    Class to navigate calendar in django

    @author Jimmy Gehloach
    """

    def __init__(self):
        pass

    @staticmethod
    def prev_month_start_end_dates(cd):

        # current month first day unaware datetime
        cm_fd_udt = f'{str(cd.year)}-{str(cd.month)}-01 23:59:59'

        # previous month last day aware datetime
        pm_ld_adt = timezone.make_aware(
            timezone.datetime.strptime(cm_fd_udt, "%Y-%m-%d %H:%M:%S") - timezone.timedelta(days=1))

        # previous month next day unaware datetime
        pm_fd_udt = f'{str(pm_ld_adt.year)}-{str(pm_ld_adt.month)}-01 00:00:00'

        # previous month last day aware datetime
        pm_fd_adt = timezone.make_aware(timezone.datetime.strptime(pm_fd_udt, "%Y-%m-%d %H:%M:%S"))

        return {
            'first_day': pm_fd_adt,
            'last_day': pm_ld_adt,
        }

    @staticmethod
    def next_month_start_end_dates(cd):
        # current month last day unaware datetime
        cm_ld_udt = f'{str(cd.year)}-{str(cd.month)}-' \
                    f'{str(calendar.monthrange(cd.year, cd.month)[1])} 00:00:00'

        # next month last day aware datetime
        nm_fd_adt = timezone.make_aware(
            timezone.datetime.strptime(cm_ld_udt, "%Y-%m-%d %H:%M:%S") + timezone.timedelta(days=1))

        # next month last day unaware datetime
        nm_ld_udt = f'{str(nm_fd_adt.year)}-{str(nm_fd_adt.month)}' \
                    f'-{str(calendar.monthrange(nm_fd_adt.year, nm_fd_adt.month)[1])} 23:59:59'

        # next month last day aware datetime
        nm_ld_adt = timezone.make_aware(timezone.datetime.strptime(nm_ld_udt, "%Y-%m-%d %H:%M:%S"))

        return {
            'first_day': nm_fd_adt,
            'last_day': nm_ld_adt,
        }

    @staticmethod
    def current_month_start_end_dates(cd):

        # current month first day unaware datetime
        cm_fd_udt = f'{str(cd.year)}-{str(cd.month)}-1 00:00:00'

        # current month last day unaware datetime
        cm_ld_udt = f'{str(cd.year)}-{str(cd.month)}-' \
                    f'{str(calendar.monthrange(cd.year, cd.month)[1])} 23:59:59'

        # current month first day aware datetime
        cm_fd_adt = timezone.make_aware(timezone.datetime.strptime(cm_fd_udt, "%Y-%m-%d %H:%M:%S"))

        # current month last day aware datetime
        cm_ld_adt = timezone.make_aware(timezone.datetime.strptime(cm_ld_udt, "%Y-%m-%d %H:%M:%S"))

        return {
            'first_day': cm_fd_adt,
            'last_day': cm_ld_adt,
        }

    @staticmethod
    def get_datetime_range_by_month(months):
        now = timezone.now()

        start_year = now.year
        start_month = now.month

        end_year = now.year
        end_month = start_month

        if int(months) > 1:
            end_month = int(end_month) + int(months)

        # if month exceeds 12 i.e. the range moved to next year
        if end_month > 12:
            end_month = end_month - 12
            end_year = int(start_year) + 1

        x, total_days = calendar.monthrange(end_year, end_month)
        start = timezone.make_aware(timezone.datetime(start_year, start_month, now.day, 0, 0, 0))
        end = timezone.make_aware(timezone.datetime(end_year, end_month, total_days, 11, 59, 59))

        return {
            'first_day': start,
            'last_day': end
        }
