import os

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel

from ehms.core.utils import verhoeff_random_number
from ehms.hospitals.models import Hospital
from ehms.patients.models import Patient
from ehms.practitioners.models import Practitioner

# TODO: move to utls
from ehms.utils.helpers import CC


def medical_session_hard_file_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"medical_session/hard_files/{now:%Y/%m}/{instance.pk}{extension}"


def medical_session_supporting_doc_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"medical_session/supporting_documents/{now:%Y/%m}/{instance.pk}{extension}"


class Department(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=100, unique=True)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='hospital_department_creator_user')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT, )

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f'{self.name}'


class Ward(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=100, unique=True)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='hospital_ward_creator_user')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT, )
    practitioners = models.ManyToManyField('practitioners.Practitioner')

    class Meta:
        verbose_name = 'Ward'
        verbose_name_plural = 'Wards'

    def __str__(self):
        return f'{self.name}'


class Keyword(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=100, unique=True)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='keyword_creator_user')

    class Meta:
        verbose_name = 'Keyword'
        verbose_name_plural = 'Keywords'

    def __str__(self):
        return f'{self.name}'


class MedicalSession(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    uid = models.CharField(verbose_name=_('UID'), unique=True, max_length=20, blank=True, )
    emergency_session = models.BooleanField(verbose_name=_('Is this an emergency session?'), default=False)
    diagnosis = models.TextField(verbose_name=_('Diagnosis'), blank=True, )
    medication = models.TextField(verbose_name=_('Medication'), blank=True, )
    procedure = models.TextField(verbose_name=_('Procedure'), blank=True, )
    hard_file = models.FileField(verbose_name=_('Hard file upload'), upload_to='medical_sessions/hard_files/',
                                 blank=True, )
    supporting_documents = models.FileField(verbose_name=_('Supporting documents'),
                                            upload_to='medical_session_supporting_doc_upload', blank=True, )
    keywords = models.ManyToManyField(Keyword, )
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT, )
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), on_delete=models.RESTRICT,
                                related_name='medical_session_patient')
    practitioner = models.ForeignKey(Practitioner, verbose_name=_('Practitioner'), on_delete=models.RESTRICT,
                                     related_name='medical_session_practitioner')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='medical_session_creator_user', )
    department = models.ForeignKey(Department, verbose_name=_('Department'), on_delete=models.RESTRICT,
                                   related_name='medical_session_department', default='OPD')
    ward = models.ForeignKey(Ward, verbose_name=_('Ward'), on_delete=models.RESTRICT,
                             related_name='medical_session_ward', )
    creation_place = models.CharField(verbose_name=_('Where it is created?'), max_length=100, blank=True)
    ipd_status = models.CharField(verbose_name=_('Patient IPD Status'), choices=CC.IPD_MEDICAL_SESSION_STATUS,
                                  default="Not Applicable", max_length=20)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 20)
        return super(MedicalSession, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Medical Session'
        verbose_name_plural = 'Medical Sessions'

    def __str__(self):
        return f'{self.uid}'
