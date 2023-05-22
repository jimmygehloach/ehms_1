from django.conf import settings
from django.db import models
from model_utils import Choices
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel, StatusModel

from ehms.core.utils import RESPONSE_CHOICE
from ehms.hospitals.models import Hospital
from ehms.practitioners.models import Practitioner


class HospitalQuery(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    subject = models.CharField(verbose_name=_('Query'), unique=True, max_length=200)
    body = models.TextField(verbose_name=_('Body'))
    attachment = models.FileField(verbose_name=_('Attachment'), upload_to='hospitals/queries/attachments/', blank=True)
    response_status = models.CharField(verbose_name=_('Response status'), choices=RESPONSE_CHOICE, default='Pending',
                                       max_length=10)
    response = models.TextField(verbose_name=_('Response'), blank=True)
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='query_hospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='hospital_query_creator_user')

    class Meta:
        verbose_name = 'Hospital Query'
        verbose_name_plural = 'Hospital Queries'

    def __str__(self):
        return f'{self.pk}'


class PractitionerQuery(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    subject = models.CharField(verbose_name=_('Query'), unique=True, max_length=200)
    body = models.TextField(verbose_name=_('Body'))
    attachment = models.FileField(verbose_name=_('Attachment'), upload_to='hospitals/queries/attachments/', blank=True)
    response_status = models.CharField(verbose_name=_('Response status'), choices=RESPONSE_CHOICE, default='Pending',
                                       max_length=10)
    response = models.TextField(verbose_name=_('Response'), blank=True)
    practitioner = models.ForeignKey(Practitioner, verbose_name=_('Practitioner'), on_delete=models.RESTRICT)
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='practitioner_query_creator_user')

    class Meta:
        verbose_name = 'Practitioner Query'
        verbose_name_plural = 'Practitioner Queries'

    def __str__(self):
        return f'{self.pk}'

# TODO: Make inbox for other levels too
