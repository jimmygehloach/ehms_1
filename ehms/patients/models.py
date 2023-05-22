import contextlib
import datetime
import math
import os

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.datetime_safe import date
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from pilkit.processors import ResizeToFill

from ehms.addresses.models import Country, Region, District, Town, Postcode
from ehms.core.utils import GENDER_CHOICES, RELIGION_CHOICES, MARITAL_CHOICES, PREGNANCY_CHOICES, BLOOD_GROUP_CHOICES, \
    verhoeff_random_number, ADDRESS_CHOICES
from ehms.hospitals.models import Hospital
from ehms.practitioners.models import Practitioner


# TODO: move this to utils
def patient_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"patient/images/{now:%Y/%m}/{instance.pk}{extension}"


def patient_document_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"patient/documents/{now:%Y/%m}/{instance.pk}{extension}"


class AgeGroup(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=50, unique=True, )
    range_from = models.IntegerField(verbose_name=_('From'), blank=True, default=0, null=True, )
    range_to = models.IntegerField(verbose_name=_('To'), blank=True, default=0, null=True, )
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='age_group_creator_user')

    class Meta:
        verbose_name = 'Age Group'
        verbose_name_plural = 'Age Groups'

    def __str__(self):
        return f'{self.name}'


class HealthStatus(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=50, unique=True, )
    css_class = models.CharField(verbose_name=_('Class Name'), max_length=100,
                                 help_text='Class name is associated with CSS styles.')
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='health_status_creator_user')

    class Meta:
        verbose_name = 'Health Status'
        verbose_name_plural = 'Health Statuses'

    def __str__(self):
        return f'{self.name}'


class MedicalIllness(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=50, unique=True, )
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='medical_illness_creator_user')

    class Meta:
        verbose_name = 'Medical Illness'
        verbose_name_plural = 'Medical Illnesses'

    def __str__(self):
        return f'{self.name}'


class Allergy(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=50, unique=True, )
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='allergy_creator_user')

    class Meta:
        verbose_name = 'Allergy'
        verbose_name_plural = 'Allergies'

    def __str__(self):
        return f'{self.name}'


class Addiction(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=50, unique=True, )
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='addiction_creator_user')

    class Meta:
        verbose_name = 'Addiction'
        verbose_name_plural = 'Addictions'

    def __str__(self):
        return f'{self.name}'


class Patient(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')

    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=100, )
    middle_name = models.CharField(verbose_name=_('Middle Name'), max_length=100, blank=True)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=100, blank=True)
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'))
    birth_time = models.TimeField(verbose_name=_('Birth time'), blank=True, null=True, )
    gender = models.CharField(verbose_name=_('Gender'), choices=GENDER_CHOICES, max_length=11)
    religion = models.CharField(verbose_name=_('Religion'), choices=RELIGION_CHOICES, max_length=50, )
    marital_status = models.CharField(verbose_name=_('Marital status'), choices=MARITAL_CHOICES, max_length=10, )
    pregnancy = models.CharField(verbose_name=_('Pregnancy status'), choices=PREGNANCY_CHOICES, max_length=20, )
    children = models.IntegerField(verbose_name=_('Children'), blank=True, default=0, )
    email = models.EmailField(verbose_name=_('Email'), max_length=100, blank=True, null=True)
    blood_group = models.CharField(verbose_name=_('Blood group'), choices=BLOOD_GROUP_CHOICES, max_length=50,
                                   blank=True)
    height = models.IntegerField(verbose_name=_('Height (in cm)'), blank=True, null=True)
    weight = models.IntegerField(verbose_name=_('Weight (in kg)'), blank=True, null=True)
    disability = models.BooleanField(verbose_name=_('Disability, if any?'), default=False)
    temporary_family_info = models.TextField(verbose_name=_('Temporary family information'), blank=True)
    bcg = models.BooleanField(verbose_name=_('BCG vaccination'), default=False)
    pentavalent = models.BooleanField(verbose_name=_('Pentavalent vaccination'), default=False)
    pneumo = models.BooleanField(verbose_name=_('Pneumo vaccination'), default=False)
    polio = models.BooleanField(verbose_name=_('Polio vaccination'), default=False)
    rotarix = models.BooleanField(verbose_name=_('Rotarix vaccination'), default=False)
    measles_rubella_1 = models.BooleanField(verbose_name=_('Measles Rubella first dose'), default=False)
    measles_rubella_2 = models.BooleanField(verbose_name=_('Measles Rubella second dose'), default=False)
    dpt = models.BooleanField(verbose_name=_('DPT vaccination'), default=False)
    yellow_fever = models.BooleanField(verbose_name=_('Yellow Fever vaccination'), default=False)
    vitamin_a = models.BooleanField(verbose_name=_('Vitamin A vaccination'), default=False)
    tetanus = models.BooleanField(verbose_name=_('Tetanus vaccination'), default=False)
    tt_one_pregnant = models.BooleanField(verbose_name=_('TT1 vaccination'), default=False)
    tt_two_pregnant = models.BooleanField(verbose_name=_('TT2 vaccination'), default=False)
    tt_booster = models.BooleanField(verbose_name=_('TT Booster'), default=False)
    other_information = models.TextField(verbose_name=_('Extra information'), blank=True)
    remarks = models.TextField(verbose_name=_('Remarks'), blank=True)
    vital_status = models.BooleanField(verbose_name=_('Vital status'), default=True)
    voter_card_number = models.CharField(max_length=100, blank=True, )
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='patient_hospital')
    health_status = models.ForeignKey(HealthStatus, verbose_name=_('Health Status'), blank=True, null=True,
                                      on_delete=models.RESTRICT, related_name='patient_health_status')
    age_group = models.ForeignKey(AgeGroup, verbose_name=_('Age Group'), on_delete=models.RESTRICT,
                                  related_name='patient_age_group', blank=True, null=True)
    patient_medical_illness = models.ManyToManyField(MedicalIllness, verbose_name=_('Patient medical illness'),
                                                     blank=True, related_name='patient_medical_illness')
    patient_kin_medical_illness = models.ManyToManyField(MedicalIllness, verbose_name=_('Patient kin medical illness'),
                                                         blank=True, related_name='patient_kin_medical_illness')
    patient_allergies = models.ManyToManyField(Allergy, verbose_name=_('Patient medical allergies'), blank=True,
                                               related_name='patient_medical_allergies')
    patient_addictions = models.ManyToManyField(Addiction, verbose_name=_('Patient addictions'), blank=True,
                                                related_name='patient_addictions')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='patient_creator_user')

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

    def get_full_name(self):
        return self.first_name + ' ' + self.middle_name + ' ' + self.last_name

    def save(self, *args, **kwargs):
        if self.date_of_birth:  # TODO: age_group
            today = date.today()
            years = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )

            if years < 1:
                months = (today.year - self.date_of_birth.year) * 12 + (today.month - self.date_of_birth.month)
                if months < 2 or months == 0:
                    self.age_group = AgeGroup.objects.filter(name='New Born').first()
                else:
                    self.age_group = AgeGroup.objects.filter(name='Infant').first()
            elif 1 <= years <= 4:
                self.age_group = AgeGroup.objects.filter(name='Toddler').first()
            elif 4 < years <= 10:
                self.age_group = AgeGroup.objects.filter(name='Child').first()
            elif 10 < years <= 18:
                self.age_group = AgeGroup.objects.filter(name='Adolescent').first()
            elif 18 < years <= 30:
                self.age_group = AgeGroup.objects.filter(name='Young Adult').first()
            elif 30 < years <= 45:
                self.age_group = AgeGroup.objects.filter(name='Middle Aged Adult').first()
            elif 45 < years <= 60:
                self.age_group = AgeGroup.objects.filter(name='Old Aged Adult').first()
            elif 60 < years <= 200:
                self.age_group = AgeGroup.objects.filter(name='Elder').first()

        if self._state.adding:
            self.uid = verhoeff_random_number(1, 12)

        return super(Patient, self).save(*args, **kwargs)

    @property
    def age(self):
        today = timezone.localdate()
        dob = datetime.datetime.strptime("1998-01-11", "%Y-%m-%d").date()
        x = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        delta = today - dob
        days = delta.days
        if x < 0:
            x = None
        elif x < 1:
            if days <= 1:
                x = f'{days} day'
            elif days < 31:
                x = f'{days} days'
            else:
                x = f'{math.floor(days / 30)} months'
        elif x == 1:
            x = f'{x} year'
        elif x > 1:
            x = f'{x} years'
        return x

    @property
    def bmi(self):
        """
        defaults
        """
        msg = ''
        height = 0
        weight = 0

        if self.height is not None:
            height = float(self.height)

        if self.weight is not None:
            weight = float(self.weight)

        if height == 0 or weight == 0:
            bmi = 0
        else:
            bmi = weight / (height / 100) ** 2

        if bmi == 0:
            msg = "You did not provide weight & height."
        elif bmi <= 18.4:
            msg = "You are underweight."
        elif bmi <= 24.9:
            msg = "You are healthy."
        elif bmi <= 29.9:
            msg = "You are over weight."
        elif bmi <= 34.9:
            msg = "You are severely over weight."
        elif bmi <= 39.9:
            msg = "You are obese."
        else:
            msg = "You are severely obese."

        return msg

    def __str__(self):
        return f'{self.uid}: {self.first_name} {self.middle_name} {self.last_name}'


class PatientImage(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    image = models.ImageField(verbose_name=_("Patient Image"), upload_to=patient_image_upload, blank=True, null=True)
    current_image = models.BooleanField(verbose_name=_('Current image'), default=False)
    image_medium = ImageSpecField([ResizeToFill(500, 500)], source='image', format='JPEG', options={'quality': 100})
    image_thumbnail = ImageSpecField([ResizeToFill(100, 100)], source='image', format='JPEG', options={'quality': 100})
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.RESTRICT,
                                related_name='patient_image')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='patient_image_hospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='patient_image_creator_user')

    def delete(self, *args, **kwargs):
        from django.core.files.storage import default_storage
        # TODO add this to other models where images are uploaded
        if self.image:
            with contextlib.suppress(FileNotFoundError):
                default_storage.delete(self.image_medium.path)
                default_storage.delete(self.image_thumbnail.path)
                self.image.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Patient Image'
        verbose_name_plural = 'Patients Image'

    def save(self, *args, **kwargs):
        if self.current_image and self.current_image is True:
            with transaction.atomic():
                PatientImage.objects.filter(
                    current_image=True,
                    patient=self.patient
                ).update(current_image=False)

        return super(PatientImage, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.patient.first_name} {self.patient.last_name}'


class PatientDocument(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=255)
    type = models.CharField(verbose_name=_('Type'), max_length=255)
    document = models.FileField(verbose_name=_('Document file'), upload_to='patient_document_upload', )
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.RESTRICT,
                                related_name='patient_document')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='patient_document_hospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='patient_document_creator_user')

    def delete(self, *args, **kwargs):
        if self.document:
            self.document.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Patient Document'
        verbose_name_plural = 'Patient Documents'

    def __str__(self):
        return f'{self.name}'


# TODO: Download option and its tracking


class PatientAddress(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')

    address_line_1 = models.CharField(verbose_name=_('Address Line 1'), max_length=250,
                                      help_text=_('e.g. Flat No or House No ...'))
    address_line_2 = models.CharField(verbose_name=_('Address Line 2'), max_length=250, blank=True,
                                      help_text=_('Extra information related to address e.g. landmark ...'))
    email = models.EmailField(verbose_name=_('Email'), blank=True, )
    phone = models.CharField(verbose_name=_('Phone'), max_length=12, blank=True)
    alternate_phone = models.CharField(verbose_name=_('Alternate Phone'), max_length=12, blank=True)
    type = models.CharField(verbose_name=_('Type'), choices=ADDRESS_CHOICES, max_length=10, default='Permanent')
    current_address = models.BooleanField(verbose_name=_('Is this your current address?'), default=False)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT,
                                related_name='patient_country')
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.RESTRICT,
                               related_name='patient_region', )
    district = models.ForeignKey(District, verbose_name=_('District'), on_delete=models.RESTRICT,
                                 related_name='patient_district')
    town = models.ForeignKey(Town, verbose_name=_('Town'), on_delete=models.RESTRICT, related_name='patient_town')
    postcode = models.ForeignKey(Postcode, verbose_name=_('PostalCode'), on_delete=models.RESTRICT,
                                 related_name='patient_postcode')
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.RESTRICT,
                                related_name='patient_belong_to_address')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='patient_address_creator_user')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='address_recorded_in_hospital')

    class Meta:
        verbose_name = 'Patient Address'
        verbose_name_plural = 'Patient Addresses'

    def save(self, *args, **kwargs):
        # TODO TRY Except
        if self.current_address and self.current_address is True:
            with transaction.atomic():
                PatientAddress.objects.filter(
                    current_address=True,
                    patient=self.patient
                ).update(current_address='False')

        if self.type and self.type == 'Permanent':
            with transaction.atomic():
                PatientAddress.objects.filter(
                    type='Permanent',
                    patient=self.patient
                ).update(type='Temporary')

        return super(PatientAddress, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.address_line_1} {self.region} {self.district}'


class PatientDeathRecord(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    died_on = models.DateTimeField(verbose_name=_('Patient death date'), default=timezone.now)
    reason = models.TextField(verbose_name=_('Reason of death'))
    place = models.CharField(verbose_name=_('Place where patient died'), max_length=200, )
    notes = models.TextField(verbose_name=_('Extra information (notes)'), max_length=20000, blank=True)
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.RESTRICT,
                                related_name='patient_died')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='patient_death_hospital')
    practitioner = models.ForeignKey(Practitioner, verbose_name=_('Practitioner'), on_delete=models.RESTRICT,
                                     related_name='patient_death_practitioner',
                                     help_text='Practitioner attended or declare the patient/dead.')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='patient_death_creator_user')

    class Meta:
        verbose_name = 'Patient Death Record'
        verbose_name_plural = 'Patient Death Record'

    def __str__(self):
        return f'{self.pk}'
