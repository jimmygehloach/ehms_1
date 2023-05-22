from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel

from ehms.core.utils import RELATIONS
from ehms.hospitals.models import Hospital
from ehms.patients.models import Patient


class FamilyTree(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    first_patient = models.ForeignKey(Patient, verbose_name=_('First Patient'), on_delete=models.RESTRICT,
                                      related_name='relation_first_patient', )
    relation = models.CharField(verbose_name=_('Select the relation'), max_length=100, choices=RELATIONS)
    second_patient = models.ForeignKey(Patient, verbose_name=_('Second Patient'), on_delete=models.RESTRICT,
                                       related_name='relation_second_patient', )
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='family_tree_creator_user')
    hospital = models.ForeignKey(Hospital, verbose_name=_('Hospital'), on_delete=models.RESTRICT,
                                 related_name='relation_hospital', )

    class Meta:
        verbose_name = 'Family Tree'
        verbose_name_plural = 'Family Tree'
