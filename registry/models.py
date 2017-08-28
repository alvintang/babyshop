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

    delivery_options = (('venue','Venue'),('address','Home Address'))
    due_date_options = (('due_date','Due Date'),('baby_birthdate','Baby Birthdate'))

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='id', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    id = models.AutoField(primary_key=True)
    event_description = models.CharField(max_length=1000, null=True)
    event_date = models.DateTimeField(null=True, blank=False)
    event_venue = models.CharField(max_length=255, blank=False)
    name_baby = models.CharField(max_length=255, blank=False)
    name_mother = models.CharField(max_length=255, blank=False)
    name_father = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    delivered_where = models.CharField(choices=delivery_options,max_length=30, blank=False)
    bool_due_date = models.CharField(choices=due_date_options,max_length=30, blank=False)
    birth_or_due_date = models.DateField(blank=True, null=True)

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
    slug = extension_fields.AutoSlugField(populate_from='id', blank=True)
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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='id', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    bought_by = models.TextField(max_length=1000, null=True, blank=True)
    message = models.TextField(max_length=10000, null=True, blank=True)
    bought = models.BooleanField()
    price_from_vendor = models.DecimalField(max_digits=12, decimal_places=2)
    price_display = models.DecimalField(max_digits=12, decimal_places=2)
    item_url = models.TextField(max_length=300)
    img_url =  models.TextField(max_length=300) 
    item_notes = models.TextField(max_length=300)
    quantity = models.IntegerField()
    quantity_bought = models.IntegerField()

    # Relationship Fields
    registry = models.ForeignKey('registry.Registry', )
    # item = models.ForeignKey('registry.Item', )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('registry_registryitem_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('registry_registryitem_update', args=(self.slug,))


