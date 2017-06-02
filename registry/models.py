from django.core.urlresolvers import reverse
from django_extensions.db.fields import AutoSlugField
from django.db.models import *
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.db import models as models
from django_extensions.db import fields as extension_fields


class Registry(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    id = models.AutoField(primary_key=True)
    event_description = models.CharField(max_length=1000, null=True)
    event_date = models.DateTimeField(null=True, blank=False)

    # Relationship Fields
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('registry_registry_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('registry_registry_update', args=(self.slug,))


class Item(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    url = models.TextField(max_length=1000)
    img_url = models.TextField(max_length=1000)
    id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=1000)

    # Relationship Fields
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('registry_item_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('registry_item_update', args=(self.slug,))


class RegistryItem(models.Model):

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    bought_by = models.TextField(max_length=100, null=True, blank=True)
    message = models.TextField(max_length=1000, null=True, blank=True)
    bought = models.BooleanField()
    price_from_vendor = models.TextField(max_length=100)
    price_display = models.TextField(max_length=100)
    vendor = models.TextField(max_length=100)

    # Relationship Fields
    registry = models.ForeignKey('registry.Registry', )
    item = models.ForeignKey('registry.Item', )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('registry_registryitem_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('registry_registryitem_update', args=(self.slug,))


