import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
#from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.CharField(max_length=255, unique=True, null=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    tel_no = models.CharField(max_length=10, blank=False)
    mobile = models.CharField(max_length=15, blank=False)
    facebook = models.CharField(max_length=255, blank=False)
    instagram = models.CharField(max_length=255, blank=False)
