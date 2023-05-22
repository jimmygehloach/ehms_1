import os

from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from pilkit.processors import ResizeToFill

from ehms.addresses.models import Country, Region, District, Town, Postcode
from ehms.core.utils import BLOOD_GROUP_CHOICES, RELIGION_CHOICES, GENDER_CHOICES, verhoeff_random_number, \
    PULSE_CHOICES, TEMPERATURE_CHOICES
from ehms.hospitals.models import Hospital
from ehms.medical_sessions.models import Department, Ward, MedicalSession
from ehms.patients.models import Patient


def nurse_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"nurse/images/{now:%Y/%m}/{instance.pk}{extension}"


class Nurse(TimeStampedModel, StatusModel, models.Model):
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
    image = models.ImageField(verbose_name=_("Nurse Image"), upload_to=nurse_image_upload, blank=True, null=True)
    image_medium = ImageSpecField([ResizeToFill(500, 500)], source='image', format='JPEG', options={'quality': 100})
    image_thumbnail = ImageSpecField([ResizeToFill(100, 100)], source='image', format='JPEG', options={'quality': 100})
    email = models.EmailField(verbose_name=_('Email'), max_length=100, null=True, blank=True)
    remarks = models.TextField(verbose_name=_('Remarks'), blank=True)
    token = models.CharField(verbose_name=_('Login token'), blank=True, null=True, max_length=8, )
    token_timestamp = models.DateTimeField(verbose_name=_('Token timestamp'), blank=True, null=True, default=None, )
    verify_token = models.BooleanField(default=False)
    phone = models.CharField(verbose_name=_('Phone'), max_length=15)
    alternate_phone = models.CharField(verbose_name=_('Alternate phone'), max_length=15, blank=True)
    address_line_1 = models.CharField(verbose_name=_('Address Line 1'), max_length=200)
    address_line_2 = models.CharField(verbose_name=_('Address Line 2'), max_length=200, blank=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT,
                                related_name='nurse_country')
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.RESTRICT, related_name='nurse_region')
    district = models.ForeignKey(District, verbose_name=_('District'), on_delete=models.RESTRICT,
                                 related_name='nurse_district')
    town = models.ForeignKey(Town, verbose_name=_('Town'), on_delete=models.RESTRICT, related_name='nurse_town')
    postcode = models.ForeignKey(Postcode, verbose_name=_('PostalCode'), on_delete=models.RESTRICT,
                                 related_name='nurse_postcode')
    hospital = models.ManyToManyField(Hospital, through='NurseHospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='nurse_creator_user')

    class Meta:
        verbose_name = 'Nurse'
        verbose_name_plural = 'Nurses'

    @property
    def age(self):
        if self.date_of_birth:
            return int((timezone.now().date() - self.date_of_birth).days / 365.25)
        return None

    @property
    def expires_in(self):
        if self.token_timestamp is None:
            return 'No Token Assigned'

        if self.token_timestamp < timezone.now():
            return 'Token Expired'
        else:
            return self.token_timestamp

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 8)
        return super(Nurse, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.uid}: {self.first_name} {self.middle_name} {self.last_name}'


class NurseHospital(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    joined_on = models.DateField(verbose_name=_('Joined on'))
    relieved_on = models.DateField(verbose_name=_('Relieved on'), blank=True, null=True)
    designation = models.CharField(verbose_name=_('Designation'), max_length=50, blank=True)
    current_hospital = models.BooleanField(verbose_name=_('Current hospital'), default=False)
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT)
    nurse = models.ForeignKey(Nurse, verbose_name=_('Nurse'), on_delete=models.RESTRICT,
                              related_name='hospital_belong_to_nurse')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='nurse_hospital_creator_user')

    class Meta:
        verbose_name = 'Nurse Hospital Record'
        verbose_name_plural = 'Nurse Hospital Records'

    def save(self, *args, **kwargs):
        if self.current_hospital and self.current_hospital is True:
            with transaction.atomic():
                NurseHospital.objects.filter(
                    current_hospital=True,
                    nurse=self.nurse
                ).update(current_hospital=False)

        return super(NurseHospital, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.nurse.first_name} {self.nurse.last_name}'


class VitalSignRecord(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    timings = models.DateTimeField(default=timezone.now)
    bed_number = models.CharField(max_length=50, )
    pulse = models.PositiveIntegerField(verbose_name=_('Pulse'), choices=PULSE_CHOICES, )
    temperature = models.PositiveIntegerField(verbose_name=_('Temperature'), choices=TEMPERATURE_CHOICES,
                                              help_text='Temperature in Fahrenheit')
    blood_pressure_systolic = models.PositiveIntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)],
                                                          blank=True, null=True,
                                                          help_text='Systolic mm Hg (upper number)')
    blood_pressure_diastolic = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)],
                                                   blank=True, null=True, help_text='Diastolic mm Hg (lower number)')
    height = models.IntegerField(validators=[MaxValueValidator(500), MinValueValidator(0)], blank=True, null=True,
                                 help_text='Height in centimeters')
    weight = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)], blank=True, null=True,
                                 help_text='Weight in kilograms')
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.RESTRICT,
                                related_name='patient_vital_sign_record')
    medical_session = models.ForeignKey(MedicalSession, verbose_name=_('Medical Session'), on_delete=models.RESTRICT,
                                        related_name='vital_sign_record_medical_session', )
    nurse = models.ForeignKey(Nurse, verbose_name=_('Nurse'), on_delete=models.RESTRICT,
                              related_name='nurse_vital_sign_record')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='vital_sign_record_hospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='vital_sign_record_creator_user')

    class Meta:
        verbose_name = 'Vital Sign Record'
        verbose_name_plural = 'Vital Sign Records'

    def __str__(self):
        return f'{self.pk}'


class IntakeOutputChart(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    intake_timings = models.DateTimeField(default=timezone.now)
    output_timings = models.DateTimeField(default=timezone.now)
    bed_number = models.CharField(max_length=50, )
    intake_oral = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)], blank=True, null=True,
                                      help_text='Write the count in digits')
    intake_iv_fluids = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)], blank=True,
                                           null=True, help_text='Write the count in digits')
    output_urine = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)], blank=True,
                                       null=True, help_text='Write the count in milliliter')
    output_vomit = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)], blank=True,
                                       null=True, help_text='Write the count in digits')
    output_suction = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)], blank=True,
                                         null=True, help_text='Write the count in digits')
    output_drain = models.IntegerField(validators=[MaxValueValidator(1000), MinValueValidator(0)], blank=True,
                                       null=True, help_text='Write the count in digits')
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.RESTRICT,
                                related_name='patient_intake_output_chart')
    medical_session = models.ForeignKey(MedicalSession, verbose_name=_('Medical Session'), on_delete=models.RESTRICT,
                                        related_name='intake_output_chart_medical_session', )
    nurse = models.ForeignKey(Nurse, verbose_name=_('Nurse'), on_delete=models.RESTRICT,
                              related_name='nurse_intake_output_chart')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='intake_output_chart_hospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='intake_output_chart_creator_user')

    class Meta:
        verbose_name = 'Intake Output Chart'
        verbose_name_plural = 'Intake Output Charts'

    def __str__(self):
        return f'{self.pk}'


def validate_observation_min_length(value):
    if value is not None or '':
        if len(value) < 10:
            raise ValidationError("Minimum length of observation is 10 characters.")


class NurseNotes(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    timings = models.DateTimeField(verbose_name=_('Date and time when note is taken'), default=timezone.now)
    bed_number = models.CharField(verbose_name=_('Bed Number'), max_length=50, )
    observation = models.TextField(verbose_name=_('Observation'), validators=[validate_observation_min_length],
                                   max_length=100000, help_text='Include medication and treatment when indicated')
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.RESTRICT,
                                related_name='patient_nurse_note')
    medical_session = models.ForeignKey(MedicalSession, verbose_name=_('Medical Session'), on_delete=models.RESTRICT,
                                        related_name='nurse_notes_medical_session', )
    nurse = models.ForeignKey(Nurse, verbose_name=_('Nurse'), on_delete=models.RESTRICT,
                              related_name='nurse_note_belong_to_nurse')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='nurse_note_record_hospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='nurse_note_creator_user')

    class Meta:
        verbose_name = 'Nurse Note'
        verbose_name_plural = 'Nurse Notes'

    def __str__(self):
        return f'{self.pk}'
