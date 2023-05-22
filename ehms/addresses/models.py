from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db import models

from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel

from ehms.core.utils import verhoeff_random_number


class Country(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(unique=True, verbose_name=_('Name'), max_length=100)
    population = models.BigIntegerField(verbose_name=_('Population'), blank=True, null=True)
    capital = models.CharField(verbose_name=_('Capital'), max_length=100, blank=True, null=True, )
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='country_creator_user')
    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 8)
        return super(Country, self).save(*args, **kwargs)


class Region(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    population = models.BigIntegerField(verbose_name=_('Population'), blank=True, null=True)
    capital = models.CharField(verbose_name=_('Capital'), max_length=100, blank=True, null=True, )
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT,
                                related_name="regions_country")
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='region_creator_user')
    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = _('Region or county')
        verbose_name_plural = _('Regions or counties')

    def __str__(self):
        if self.status == 'active':
            n = f'{self.name}'
        else:
            n = f'{self.name}'
        return f'{n}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 8)
        return super(Region, self).save(*args, **kwargs)


class District(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    population = models.BigIntegerField(verbose_name=_('Population'), blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT,
                                related_name='districts_country')
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.RESTRICT,
                               related_name="districts_region")
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='district_creator_user')
    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 8)
        return super(District, self).save(*args, **kwargs)


class Town(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name of Town'), max_length=100)
    population = models.BigIntegerField(verbose_name=_('Population of Town'), blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT,
                                related_name="towns_country")
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.RESTRICT, related_name="towns_region")
    district = models.ForeignKey(District, verbose_name=_('District'), on_delete=models.RESTRICT,
                                 related_name='towns_district')
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='town_creator_user')
    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = _('Town or City')
        verbose_name_plural = _('Towns or Cities')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 8)
        return super(Town, self).save(*args, **kwargs)


class Postcode(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(verbose_name=_('Name of Postcode'), max_length=100)
    population = models.BigIntegerField(verbose_name=_('Population of Postcode'), blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT,
                                related_name="postcodes_country")
    region = models.ForeignKey(Region, verbose_name=_('Region'), on_delete=models.RESTRICT,
                               related_name="postcodes_region")
    district = models.ForeignKey(District, verbose_name=_('District'), on_delete=models.RESTRICT,
                                 related_name="postcodes_district")
    town = models.ForeignKey(Town, verbose_name=_('Town'), on_delete=models.RESTRICT, related_name="postcodes_town")
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='postcode_creator_user')
    uid = models.CharField(verbose_name=_('UID'), max_length=255, unique=True, blank=True)

    class Meta:
        verbose_name = _('Postcode')
        verbose_name_plural = _('Postcodes')

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.uid = verhoeff_random_number(1, 8)
        return super(Postcode, self).save(*args, **kwargs)
