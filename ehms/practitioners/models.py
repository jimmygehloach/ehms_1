import contextlib
import os

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from pilkit.processors import ResizeToFill

from ehms.addresses.models import Country, Region, District, Town, Postcode
from ehms.core.utils import BLOOD_GROUP_CHOICES, RELIGION_CHOICES, GENDER_CHOICES, verhoeff_random_number
from ehms.hospitals.models import Hospital


# TODO: shift to utils file
def practitioner_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"practitioner/images/{now:%Y/%m}/{instance.pk}{extension}"


class Practitioner(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=100, )
    middle_name = models.CharField(verbose_name=_('Middle Name'), max_length=100, blank=True)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=100, blank=True)
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'), blank=True, null=True, )
    vital_status = models.BooleanField(verbose_name=_('Vital status'), default=True)
    blood_group = models.CharField(verbose_name=_('Blood group'), choices=BLOOD_GROUP_CHOICES, max_length=50,
                                   blank=True)
    religion = models.CharField(verbose_name=_('Religion'), choices=RELIGION_CHOICES, max_length=50, blank=True)
    gender = models.CharField(verbose_name=_('Gender'), choices=GENDER_CHOICES, max_length=11, blank=True)
    image = models.ImageField(verbose_name=_("Practitioner Image"), upload_to=practitioner_image_upload, blank=True,
                              null=True)
    image_medium = ImageSpecField([ResizeToFill(500, 500)], source='image', format='JPEG', options={'quality': 100})
    image_thumbnail = ImageSpecField([ResizeToFill(100, 100)], source='image', format='JPEG', options={'quality': 100})
    email = models.EmailField(verbose_name=_('Email'), max_length=100)
    remarks = models.TextField(verbose_name=_('Remarks'), blank=True)
    token = models.CharField(verbose_name=_('Login token'), blank=True, null=True, max_length=8, )
    token_timestamp = models.DateTimeField(verbose_name=_('Token timestamp'), blank=True, null=True, default=None, )
    verify_token = models.BooleanField(default=False)
    phone = models.CharField(verbose_name=_('Phone'), max_length=15)
    alternate_phone = models.CharField(verbose_name=_('Alternate phone'), max_length=15, blank=True)
    address_line_1 = models.CharField(verbose_name=_('Address Line 1'), max_length=200)
    address_line_2 = models.CharField(verbose_name=_('Address Line 2'), max_length=200, blank=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT)
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.RESTRICT)
    district = models.ForeignKey(District, verbose_name=_('District'), on_delete=models.RESTRICT)
    town = models.ForeignKey(Town, verbose_name=_('Town'), on_delete=models.RESTRICT)
    postcode = models.ForeignKey(Postcode, verbose_name=_('PostalCode'), on_delete=models.RESTRICT)
    hospital = models.ManyToManyField(Hospital, through='PractitionerHospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='practitioner_creator_user')

    class Meta:
        verbose_name = 'Practitioner'
        verbose_name_plural = 'Practitioners'

    @property
    def expires_in(self):
        if self.token_timestamp is None:
            return 'No Token Assigned'

        if self.token_timestamp < timezone.now():
            return 'Token Expired'
        else:
            return self.token_timestamp

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage
        if self.image:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(self.image_medium.path)
                default_storage.delete(self.image_thumbnail.path)
                self.image.delete()
        super().delete(*args, **kwargs)

    def get_full_name(self):
        return self.first_name + ' ' + self.middle_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 8)
        return super(Practitioner, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.uid}: {self.first_name} {self.last_name}'


class PractitionerHospital(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    joined_on = models.DateField(verbose_name=_('Practitioner Joined on'))
    relieved_on = models.DateField(verbose_name=_('Practitioner Relieved on'), blank=True, null=True)
    designation = models.CharField(verbose_name=_('Designation'), max_length=50)
    current_hospital = models.BooleanField(verbose_name=_('Current hospital'), default=False)
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='practitioner_hospital')
    practitioner = models.ForeignKey(Practitioner, verbose_name=_('Practitioner'), on_delete=models.RESTRICT,
                                     related_name='practitioner_hospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='practitioner_hospital_creator_user')

    class Meta:
        verbose_name = 'Practitioner Hospital Record'
        verbose_name_plural = 'Practitioner Hospital Records'

    def save(self, *args, **kwargs):
        if self.current_hospital and self.current_hospital is True:
            with transaction.atomic():
                PractitionerHospital.objects.filter(
                    current_hospital=True,
                    practitioner=self.practitioner
                ).update(current_hospital=False)

        return super(PractitionerHospital, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.pk}'
