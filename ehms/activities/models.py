from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices

from model_utils.models import TimeStampedModel, StatusModel

from ehms.hospitals.models import Hospital
from ehms.patients.models import Patient


class Activity(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Logged in user'), blank=True, null=True,
                                     on_delete=models.RESTRICT, related_name='activity_creator_user')
    activity_level = models.CharField(verbose_name=_('Activity Level'), max_length=200, blank=True, null=True, )
    action = models.CharField(verbose_name=_('Action'), max_length=100, blank=True, null=True, )
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'), blank=True, null=True, on_delete=models.RESTRICT)
    hospital = models.ForeignKey(Hospital, blank=True, null=True, verbose_name=_('Hospital'), on_delete=models.RESTRICT)
    user_group = models.CharField(verbose_name=_('User Group'), max_length=200, blank=True, null=True, )
    uid = models.CharField(verbose_name=_('User UID'), blank=True, null=True, max_length=200)
    description = models.TextField(verbose_name=_('Description of activity'), blank=True, null=True, )
    user_agent = models.TextField(verbose_name=_('User agent'), blank=True, null=True, )
    ip_address = models.CharField(verbose_name=_('IP address'), max_length=200, blank=True, null=True, )
    ip_routable = models.CharField(verbose_name=_('IP routable'), max_length=200, blank=True, null=True, )

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'
