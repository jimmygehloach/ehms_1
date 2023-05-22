import os

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from model_utils import Choices
from model_utils.models import UUIDModel, TimeStampedModel, StatusModel
from pilkit.processors import ResizeToFill

from ehms.addresses.models import Country
from ehms.core.utils import INVENTORY_STOCK_TYPE, verhoeff_random_number
from ehms.hospitals.models import Hospital
from ehms.medical_sessions.models import Department


def item_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"item/images/{now:%Y/%m}/{instance.pk}{extension}"


def supplier_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"supplier/images/{now:%Y/%m}/{instance.pk}{extension}"


class ItemCategory(UUIDModel, TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(
        verbose_name=_('Name'),
        unique=True,
        max_length=200
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True
    )
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Logged in user'),
        on_delete=models.RESTRICT,
        related_name='item_category_creator_user'
    )

    class Meta:
        verbose_name = 'Item Category'
        verbose_name_plural = 'Item Categories'

    def __str__(self):
        return f'{self.name}'


class Item(UUIDModel, TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    item_name = models.CharField(
        verbose_name=_('Item Name'),
        unique=True,
        max_length=200
    )
    sku = models.CharField(
        verbose_name=_('SKU'),
        max_length=255,
        blank=True,
        null=True,
        unique=True
    )
    market_price = models.DecimalField(
        verbose_name=_('Market Price'),
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2
    )
    selling_price = models.DecimalField(
        verbose_name=_('Selling Price'),
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2
    )
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True
    )
    minimum_stock_value = models.PositiveIntegerField(
        verbose_name=_('Minimum Stock Value'),
        validators=[MaxValueValidator(100000000), MinValueValidator(1)],
    )
    item_category = models.ForeignKey(
        ItemCategory,
        verbose_name=_('Item Category'),
        on_delete=models.RESTRICT,
        related_name='item_category',
    )
    image = models.ImageField(
        verbose_name=_("Item Image"),
        upload_to=item_image_upload,
        blank=True,
        null=True
    )
    image_medium = ImageSpecField([
        ResizeToFill(500, 500)],
        source='image',
        format='JPEG',
        options={'quality': 100}
    )
    image_thumbnail = ImageSpecField([
        ResizeToFill(100, 100)],
        source='image',
        format='JPEG',
        options={'quality': 100}
    )
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Logged in user'),
        on_delete=models.RESTRICT,
        related_name='item_creator_user'
    )

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return f'{self.item_name}'


class Supplier(UUIDModel, TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(
        verbose_name=_('Name'),
        max_length=200
    )
    company = models.CharField(
        verbose_name=_('Company'),
        max_length=200
    )
    email = models.EmailField(
        verbose_name=_('Email'),
        max_length=100,
        blank=True
    )
    phone = models.CharField(
        verbose_name=_('Phone'),
        max_length=12
    )
    alternate_phone = models.CharField(
        verbose_name=_('Alternate phone'),
        max_length=12,
        blank=True
    )
    address_line_1 = models.CharField(
        verbose_name=_('Address Line 1'),
        max_length=200
    )
    address_line_2 = models.CharField(
        verbose_name=_('Address Line 2'),
        max_length=200,
        blank=True,
        help_text='Landmark near by, if any'
    )
    city = models.CharField(
        verbose_name=_('City'),
        max_length=200,
    )
    country = models.CharField(
        verbose_name=_('Country'),
        max_length=200,
    )
    postcode = models.CharField(
        verbose_name=_('Postcode'),
        max_length=200,
    )
    image = models.ImageField(
        verbose_name=_("Supplier Image"),
        upload_to=supplier_image_upload,
        blank=True,
        null=True
    )
    image_medium = ImageSpecField([
        ResizeToFill(500, 500)],
        source='image',
        format='JPEG',
        options={'quality': 100}
    )
    image_thumbnail = ImageSpecField([
        ResizeToFill(100, 100)],
        source='image',
        format='JPEG',
        options={'quality': 100}
    )
    remarks = models.TextField(
        verbose_name=_('Remarks'),
        blank=True
    )
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Logged in user'),
        on_delete=models.RESTRICT,
        related_name='supplier_creator_user'
    )

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return f'{self.name} ( {self.company} )'


class ReceivedDetail(UUIDModel, TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    bill_number = models.CharField(
        verbose_name=_('Bill Number'),
        max_length=12,
        blank=True,
        unique=True,
    )
    supplier = models.ForeignKey(
        Supplier,
        verbose_name=_('Supplier'),
        on_delete=models.RESTRICT,
        related_name='supplier_of_item',
    )
    total_items = models.PositiveSmallIntegerField(
        verbose_name='Total items',
    )
    gross_amount = models.DecimalField(
        verbose_name=_('Gross Amount'),
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2,
        help_text=_('Total amount of the received items.')
    )
    remarks = models.TextField(
        verbose_name=_('Remarks'),
        max_length=10000,
        blank=True,
        help_text=_('Write something important against received items.')
    )
    hospital = models.ForeignKey(
        Hospital,
        verbose_name=_('Hospital'),
        on_delete=models.RESTRICT,
        related_name='received_hospital',
    )
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Logged in user'),
        on_delete=models.RESTRICT,
        related_name='received_creator_user'
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.bill_number = 'R-' + verhoeff_random_number(1, 10)

        return super(ReceivedDetail, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.bill_number}'


class IssuedDetail(UUIDModel, TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    bill_number = models.CharField(
        verbose_name=_('Bill Number'),
        max_length=12,
        blank=True,
        unique=True,
    )
    gross_amount = models.DecimalField(
        verbose_name=_('Gross Amount'),
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2,
        help_text=_('Total amount of the issued items.')
    )
    total_items = models.PositiveSmallIntegerField(
        verbose_name='Total items',
    )
    remarks = models.TextField(
        verbose_name=_('Remarks'),
        max_length=10000,
        blank=True,
        help_text=_('Write something important against issued items.')
    )
    department = models.ForeignKey(
        Department,
        verbose_name=_('Department'),
        on_delete=models.RESTRICT,
        related_name='issued_department',
    )
    hospital = models.ForeignKey(
        Hospital,
        verbose_name=_('Hospital'),
        on_delete=models.RESTRICT,
        related_name='issued_hospital',
    )
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Logged in user'),
        on_delete=models.RESTRICT,
        related_name='issued_creator_user'
    )

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.bill_number = 'I-' + verhoeff_random_number(1, 10)

        return super(IssuedDetail, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.bill_number}'


class Inventory(UUIDModel, TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    item_category = models.ForeignKey(
        ItemCategory,
        verbose_name=_('Item Category'),
        on_delete=models.RESTRICT,
        related_name='inventory_item_category',
    )
    item = models.ForeignKey(
        Item,
        verbose_name=_('Item'),
        on_delete=models.RESTRICT,
        related_name='inventory_item',
    )
    type = models.CharField(
        max_length=200,
        verbose_name=_('Type'),
        default='Stock In',
    )
    received_quantity = models.PositiveIntegerField(
        verbose_name=_('Received Quantity'),
        validators=[MaxValueValidator(100000000), MinValueValidator(1)],
        help_text=_('Quantity is like a unit.'),
        null=True,
        blank=True,
    )
    issued_quantity = models.PositiveIntegerField(
        verbose_name=_('Issued Quantity'),
        validators=[MaxValueValidator(100000000), MinValueValidator(1)],
        help_text=_('Quantity is like a unit.'),
        null=True,
        blank=True,
    )
    price = models.DecimalField(
        verbose_name=_('Item Price'),
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2,
        help_text=_('The price here will be per unit.')
    )
    vat = models.DecimalField(
        verbose_name=_('Vat'),
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2,
        help_text=_('Mention the price not the percentage.')
    )
    discount = models.DecimalField(
        verbose_name=_('Discount'),
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2,
        help_text=_('Mention the price not the percentage.')
    )
    total_price = models.DecimalField(
        verbose_name=_('Total Price'),
        blank=True,
        null=True,
        max_digits=9,
        decimal_places=2,
        help_text=_('Price of all the units i.e. entire quantity.')
    )
    remarks = models.TextField(
        verbose_name=_('Remarks'),
        blank=True,
        max_length=10000,
        help_text=_('Write something important against item.')
    )
    received_detail = models.ForeignKey(
        ReceivedDetail,
        blank=True,
        null=True,
        verbose_name=_('Received Detail'),
        on_delete=models.RESTRICT,
        related_name='inventory_receive_detail',
    )
    issued_detail = models.ForeignKey(
        IssuedDetail,
        blank=True,
        null=True,
        verbose_name=_('Issued Detail'),
        on_delete=models.RESTRICT,
        related_name='inventory_issue_detail',
    )
    hospital = models.ForeignKey(
        Hospital,
        verbose_name=_('Hospital'),
        on_delete=models.RESTRICT,
        related_name='inventory_hospital',
    )
    creator_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Logged in user'),
        on_delete=models.RESTRICT,
        related_name='inventory_creator_user'
    )

    class Meta:
        verbose_name = 'Inventory'
        verbose_name_plural = 'Inventory'

    def __str__(self):
        return f'{self.pk}'
