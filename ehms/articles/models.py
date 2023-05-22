import os

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from imagekit.models import ImageSpecField

from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from pilkit.processors import ResizeToFill

from ehms.addresses.models import Region, District, Country
from ehms.core.utils import ARTICLE_TYPE
from ehms.hospitals.models import Hospital


def article_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename)
    extension = extension.lower()
    return f"article/images/{now:%Y/%m}/{instance.pk}{extension}"


class ArticleCategory(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(unique=True, verbose_name=_('Title'), max_length=100)
    description = models.TextField(verbose_name=_('Description'), max_length=5000, blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='ctegory_creator_user')

    class Meta:
        verbose_name = 'Article Category'
        verbose_name_plural = 'Article Categories'

    def __str__(self):
        return self.name


class Article(TimeStampedModel, StatusModel, models.Model):
    STATUS = Choices('active', 'inactive')
    title = models.CharField(unique=True, verbose_name=_('Title'), max_length=254)
    published_at = models.DateTimeField(verbose_name=_('Published at'), blank=True, null=True, )
    published = models.BooleanField(verbose_name=_('Published'), default=False)
    excerpt = models.TextField(verbose_name=_('Excerpt'), max_length=500, blank=True)
    content = models.TextField(verbose_name=_('Content'),)
    type = models.CharField(verbose_name=_('Types'), choices=ARTICLE_TYPE, max_length=25, default='Article Other')
    image = models.ImageField(verbose_name=_("Article Image"), upload_to=article_image_upload, blank=True, null=True)
    image_article = ImageSpecField([ResizeToFill(850, 490)], source='image', format='JPEG', options={'quality': 100})
    image_medium = ImageSpecField([ResizeToFill(430, 230)], source='image', format='JPEG', options={'quality': 100})
    image_thumbnail = ImageSpecField([ResizeToFill(100, 100)], source='image', format='JPEG', options={'quality': 100})
    category = models.ForeignKey(ArticleCategory, null=True, blank=True, verbose_name=_('Category'),
                                 on_delete=models.RESTRICT, related_name='article_Category')
    country = models.ForeignKey(Country, verbose_name=_('Country'), on_delete=models.RESTRICT,
                                related_name="article_country")
    region = models.ManyToManyField(Region, blank=True)
    district = models.ManyToManyField(District, blank=True)
    hospital = models.ManyToManyField(Hospital, blank=True)
    creator_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_('Logged in user'),
                                     on_delete=models.RESTRICT, related_name='article_creator_user')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.title
