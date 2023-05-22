import contextlib
import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from model_utils import Choices
from model_utils.models import UUIDModel, TimeStampedModel, StatusModel
from pilkit.processors import ResizeToFill

from ehms.addresses.models import Country, Region, District, Town, Postcode
from ehms.core.utils import verhoeff_random_number


# TODO: make a util function for this which handles everything automatically
def hospital_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"hospital/images/{now:%Y/%m}/{instance.pk}{extension}"


# TODO: make a util function for this which handles everything automatically
def hospital_rep_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"hospital/representative/{now:%Y/%m}/{instance.pk}{extension}"


class Hospital(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)
    name = models.CharField(verbose_name=_('Name'), unique=True, max_length=200)
    email = models.EmailField(verbose_name=_('Email'), max_length=100, blank=True)
    phone = models.CharField(verbose_name=_('Phone'), max_length=15)
    alternate_phone = models.CharField(verbose_name=_('Alternate phone'), max_length=15, blank=True)
    address_line_1 = models.CharField(verbose_name=_('Address Line 1'), max_length=200)
    address_line_2 = models.CharField(verbose_name=_('Address Line 2'), max_length=200, blank=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT,
                                related_name='hospital_country', )
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.RESTRICT,
                               related_name='hospital_region', )
    district = models.ForeignKey(District, verbose_name=_('District'), on_delete=models.RESTRICT,
                                 related_name='hospital_district', )
    town = models.ForeignKey(Town, verbose_name=_('Town'), on_delete=models.RESTRICT, related_name='hospital_town', )
    postcode = models.ForeignKey(Postcode, verbose_name=_('PostalCode'), on_delete=models.RESTRICT,
                                 related_name='hospital_postcode', )
    longitude = models.CharField(verbose_name=_('Longitude'), max_length=200, blank=True)
    latitude = models.CharField(verbose_name=_('Latitude'), max_length=200, blank=True)
    beds = models.PositiveIntegerField(verbose_name=_('Beds'), default=0)
    image = models.ImageField(verbose_name=_("Hospital Image"), upload_to=hospital_image_upload, blank=True, null=True)
    image_medium = ImageSpecField([ResizeToFill(500, 500)], source='image', format='JPEG', options={'quality': 100})
    image_thumbnail = ImageSpecField([ResizeToFill(100, 100)], source='image', format='JPEG', options={'quality': 100})
    remarks = models.TextField(verbose_name=_('Remarks'), blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='hospital_creator_user')

    class Meta:
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitals'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 6)
        return super(Hospital, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage
        if self.image:  # TODO: implement image delete in other modals also
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(self.image_medium.path)
                default_storage.delete(self.image_thumbnail.path)
                self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class HospitalRepresentative(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]  # TODO: access it from utils
    first_name = models.CharField(verbose_name=_('First name'), max_length=200)
    last_name = models.CharField(verbose_name=_('Last name'), max_length=200, blank=True)
    gender = models.CharField(verbose_name=_('Gender'), choices=GENDER_CHOICES, max_length=6, blank=True)
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'), blank=True, null=True)
    phone = models.CharField(verbose_name=_('Phone number'), max_length=15)
    alternate_phone = models.CharField(verbose_name=_('Alternate phone'), max_length=15, blank=True)
    email = models.EmailField(verbose_name=_('Email'), max_length=100, blank=True)
    designation = models.CharField(verbose_name=_('Designation'), max_length=200, blank=True)
    image = models.ImageField(verbose_name=_("Representative Image"), upload_to=hospital_rep_image_upload, blank=True,
                              null=True)
    image_medium = ImageSpecField([ResizeToFill(500, 500)], source='image', format='JPEG', options={'quality': 100})
    image_thumbnail = ImageSpecField([ResizeToFill(100, 100)], source='image', format='JPEG', options={'quality': 100})
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='hospital_rep_hospital', )
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='hospital_rep_creator_user')
    remarks = models.TextField(verbose_name=_('Remarks'), blank=True)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage
        if self.image:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(self.image_medium.path)
                default_storage.delete(self.image_thumbnail.path)
                self.image.delete()
        super().delete(*args, **kwargs)

    @property
    def age(self):
        return int((timezone.now().date() - self.date_of_birth).days / 365.25)  # TODO move this in utils class

    class Meta:
        verbose_name = 'Representative'
        verbose_name_plural = 'Representatives'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    get_full_name.short_description = _("Full name")
