from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel

from ehms.core.utils import verhoeff_random_number, RELATIONS
from ehms.hospitals.models import Hospital
from ehms.patients.models import Patient


class Mortuary(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)
    name = models.CharField(verbose_name=_('Name of Mortuary'), max_length=200, )
    capacity = models.PositiveIntegerField(verbose_name=_('Capacity'),
                                           validators=[MaxValueValidator(1000), MinValueValidator(1)], )
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='mortuary_hospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='mortuary_creator_user')

    def current_capacity(self):
        in_patients = MortuaryPatient.objects.filter(
            status='active',
            in_mortuary=True,
            mortuary_id=self.pk,
        ).count()
        return self.capacity - in_patients

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 6)
        return super(Mortuary, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Mortuary'
        verbose_name_plural = 'Mortuaries'

    def __str__(self):
        return f'{self.name}'


class MortuaryPatient(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    tag = models.CharField(verbose_name=_('Random tag generated against deceased patient'), max_length=18, unique=True)
    date_received = models.DateTimeField(verbose_name=_('Mortuary entry date of deceased patient'),
                                         default=timezone.now)
    date_released = models.DateTimeField(verbose_name=_('Mortuary released date of deceased patient'), blank=True,
                                         null=True, )
    reason_behind_release = models.TextField(verbose_name=_('Reason behind release of deceased patient'), )
    in_mortuary = models.BooleanField(verbose_name=_('Is deceased patient in mortuary?'), default=True)
    next_of_kin = models.CharField(verbose_name=_('Deceased patient next of kin name'), max_length=200, blank=True)
    next_of_kin_relationship = models.CharField(verbose_name=_('Next of kin relationship to deceased patient'),
                                                max_length=100, choices=RELATIONS, blank=True)
    non_relative_person = models.CharField(verbose_name=_('Non relative person name'), max_length=200, blank=True)
    person_address = models.TextField(verbose_name=_('Person address'),
                                      help_text='Provide address of who ever released the deceased patient')
    person_phone = models.CharField(verbose_name=_('Person phone'),
                                    help_text='Provide phone of who ever released the deceased patient',
                                    max_length=12, )
    witness = models.CharField(verbose_name=_('Witness name'), blank=True, max_length=200,
                               help_text='Witness during the release of the deceased patient')
    witness_address = models.TextField(verbose_name=_('Witness address'), blank=True, help_text='Witness address')
    witness_phone = models.CharField(verbose_name=_('Witness phone'), blank=True, help_text='Witness phone',
                                     max_length=12, )
    person_uid = models.CharField(max_length=12, verbose_name='Person UID if available', blank=True)
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.RESTRICT,
                                related_name='mortuary_patient_belongs_to_patient')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='mortuary_patient_hospital')
    mortuary = models.ForeignKey(Mortuary, verbose_name=_('Mortuary'), on_delete=models.RESTRICT,
                                 related_name='mortuary_patient_mortuary')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='mortuary_patient_creator_user')

    def save(self, *args, **kwargs):
        if self._state.adding:
            # TODO: Do not let save this record if mortuary capacity gets full
            self.tag = 'M-' + verhoeff_random_number(1, 16)
        return super(MortuaryPatient, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Mortuary Patient'
        verbose_name_plural = 'Mortuary Patients'

    def __str__(self):
        return f'{self.tag}'
