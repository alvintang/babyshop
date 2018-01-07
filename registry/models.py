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
import uuid
import random
import string

class Registry(models.Model):

    delivery_options = (('venue','Venue'),('address','Home Address'))
    due_date_options = (('due_date','Due Date'),('baby_birthdate','Baby Birthdate'))

    # Fields
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='created', blank=True)
    # slug = models.SlugField(unique=True, editable=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    id = models.AutoField(primary_key=True,default=None)
    event_description = models.CharField(max_length=1000, null=True)
    event_date = models.DateTimeField(null=True, blank=False)
    event_venue = models.CharField(max_length=255, blank=False)
    name_baby = models.CharField(max_length=255, blank=False)
    name_mother = models.CharField(max_length=255, blank=False)
    name_father = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)
    delivered_where = models.CharField(choices=delivery_options,max_length=30, blank=False)
    #bool_due_date = models.CharField(choices=due_date_options,max_length=30, blank=False)
    birth_or_due_date = models.DateField(blank=False)

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

    # def save(self, *args, **kwargs):
    #     while not self.slug:
    #         ret = []
    #         # ret.extend(random.sample(string.ascii_letters, 3))
    #         ret.extend(random.sample(string.digits, 8))

    #         newslug = ''.join(ret)
    #         if Registry.objects.filter(pk=newslug).count():
    #             self.slug = newslug

    #     super(SluggedModel, self).save(*args, **kwargs)


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
    bought = models.BooleanField(default=False)
    price_from_vendor = models.DecimalField(max_digits=12, decimal_places=2)
    price_display = models.DecimalField(max_digits=12, decimal_places=2)
    item_url = models.TextField(max_length=300)
    img_url =  models.TextField(max_length=300) 
    item_notes = models.TextField(max_length=10000)
    quantity = models.IntegerField()
    quantity_bought = models.IntegerField()
    from_partner_store = models.BooleanField();
    img_shop = models.ImageField(upload_to="shop/", null=True, blank=True)

    # Relationship Fields
    registry = models.ForeignKey('registry.Registry', default=None)
    # item = models.ForeignKey('registry.Item', )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    def get_absolute_url(self):
        return reverse('registry_registryitem_detail', args=(self.slug,))


    def get_update_url(self):
        return reverse('registry_registryitem_update', args=(self.slug,))

    def registry_name(self):
        return self.registry.name
    registry_name.short_description = 'Registry Name'

    def registry_id(self):
        return self.registry.id
    registry_id.short_description = 'Registry ID'


class RegistryItemPaid(models.Model):

    # Fields
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='id', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    #name_giver = models.TextField(max_length=1000, null=True, blank=True)
    message = models.TextField(max_length=10000, null=True, blank=True)
    email = models.EmailField(blank=False)
    tel_no = models.CharField(max_length=10, blank=True)
    mobile = models.CharField(max_length=15, blank=False)
    reserved = models.BooleanField()
    paid = models.BooleanField()
    quantity = models.IntegerField()

    # Relationship Fields
    registry_item = models.ForeignKey('registry.RegistryItem', )
    transaction = models.ForeignKey('registry.Transaction', default=uuid.uuid4, )
    # item = models.ForeignKey('registry.Item', )

    class Meta:
        ordering = ('-created',)
        unique_together = (('registry_item','email'),)

    def __unicode__(self):
        return u'%s' % self.slug

    def transaction_id(self):
        return self.transaction.id
    transaction_id.short_description = 'Transaction ID'


class Transaction(models.Model):

    # Fields
    # id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = extension_fields.AutoSlugField(populate_from='id', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    message = models.TextField(max_length=10000, null=True, blank=True)
    email = models.EmailField(blank=False)
    tel_no = models.CharField(max_length=10, blank=True)
    mobile = models.CharField(max_length=15, blank=False)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2) 
    total_amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    date_paid = models.DateTimeField(null=True, blank=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationship Fields
    # registry_item = models.ForeignKey('registry.RegistryItem', )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

