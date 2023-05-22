from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from model_utils import Choices
from model_utils.models import UUIDModel, TimeStampedModel, StatusModel

from ehms.core.utils import RESPONSE_CHOICE
from ehms.hospitals.models import Hospital


class UserRequest(UUIDModel, TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    request_id = models.CharField(
        verbose_name=_('Request Id'),
        max_length=255,
        unique=True,
        blank=True
    )
    user_level = models.CharField(
        verbose_name=_('User Level'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('Describe the changes'),
        max_length=10000000
    )
    document = models.FileField(
        verbose_name=_('Upload relevant document'),
        blank=True,
        null=True,
        upload_to='patient_document_upload',
    )
    hospital = models.ForeignKey(
        Hospital,
        blank=True,
        null=True,
        verbose_name=_('Hospital'),
        on_delete=models.RESTRICT,
        related_name='user_request_hospital',
    )
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Logged in user'),
        on_delete=models.RESTRICT,
        related_name='user_request_creator_user'
    )
    response_status = models.CharField(
        verbose_name=_('Response status'),
        choices=RESPONSE_CHOICE,
        default='Pending',
        max_length=10
    )

    class Meta:
        verbose_name = 'User Request'
        verbose_name_plural = 'User Reuests'


class UserReport(UUIDModel, TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    report_id = models.CharField(
        verbose_name=_('Request Id'),
        max_length=255,
        unique=True,
        blank=True
    )
    user_level = models.CharField(
        verbose_name=_('User Level'),
        max_length=255,
    )
    section = models.CharField(
        verbose_name=_('Section'),
        max_length=255,
    )
    description = models.TextField(
        verbose_name=_('Describe the changes'),
        max_length=10000000
    )
    hospital = models.ForeignKey(
        Hospital,
        blank=True,
        null=True,
        verbose_name=_('Hospital'),
        on_delete=models.RESTRICT,
        related_name='user_report_hospital',
    )
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Logged in user'),
        on_delete=models.RESTRICT,
        related_name='user_report_creator_user'
    )
    response_status = models.CharField(
        verbose_name=_('Response status'),
        choices=RESPONSE_CHOICE,
        default='Pending',
        max_length=10
    )

    class Meta:
        verbose_name = 'User Report'
        verbose_name_plural = 'User Reports'
