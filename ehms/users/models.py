from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel

from ehms.addresses.models import Country


class UserProfile(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    ADDRESS_CHOICES = [('Temporary', 'Temporary'), ('Permanent', 'Permanent')]

    # Override the status field to set a default value
    status = models.CharField(max_length=20, choices=STATUS, default='active')

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(verbose_name=_('Gender'), choices=GENDER_CHOICES, max_length=6, blank=True)
    date_of_birth = models.DateField(verbose_name=_('Date of Birth'), blank=True, null=True)
    bio = models.TextField(verbose_name=_('Bio'), blank=True)
    designation = models.CharField(max_length=100, verbose_name=_('Designation'), blank=True)
    address_line_1 = models.CharField(verbose_name=_('Address Line 1'), max_length=100,
                                      help_text=_('e.g. Flat No or House No ...'), blank=True)
    address_line_2 = models.CharField(verbose_name=_('Address Line 2'), max_length=200, blank=True,
                                      help_text=_('Extra information related to address e.g. landmark ...'))
    phone = models.CharField(verbose_name=_('Phone'), max_length=10, blank=True)
    alternate_phone = models.CharField(verbose_name=_('Alternative Phone'), max_length=10, blank=True)
    type_of_address = models.CharField(verbose_name=_('Type of address'), choices=ADDRESS_CHOICES, max_length=10,
                                       blank=True)
    remarks = models.TextField(_('Remarks'), max_length=5000, blank=True)
    user_unique_id = models.CharField(max_length=20, blank=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT,
                                related_name="users_country", blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
