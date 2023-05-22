import contextlib
import os

from django.conf import settings
from django.db import models

# Create your models here.
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from pilkit.processors import ResizeToFill

from ehms.addresses.models import Country, District, Town, Postcode, Region
from ehms.core.utils import BLOOD_GROUP_CHOICES, RELIGION_CHOICES, GENDER_CHOICES, verhoeff_random_number
from ehms.hospitals.models import Hospital


# TODO: shift to utils file
def reception_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"receptionist/images/{now:%Y/%m}/{instance.pk}{extension}"


class Reception(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)
    name = models.CharField(verbose_name=_('Name of reception'), max_length=100, )
    token = models.CharField(verbose_name=_('Login token'), blank=True, null=True, max_length=8, )
    token_timestamp = models.DateTimeField(verbose_name=_('Token timestamp'), blank=True, null=True, default=None, )
    verify_token = models.BooleanField(default=False)
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='reception_hospital')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='reception_creator_user')

    class Meta:
        verbose_name = 'Reception'
        verbose_name_plural = 'Receptions'

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
        return super(Reception, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

