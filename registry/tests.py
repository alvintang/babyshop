import unittest
from django.core.urlresolvers import reverse
from django.test import Client
from .models import Registry, Item, RegistryItem
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def create_django_contrib_auth_models_user(**kwargs):
    defaults = {}
    defaults["username"] = "username"
    defaults["email"] = "username@tempurl.com"
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_django_contrib_auth_models_group(**kwargs):
    defaults = {}
    defaults["name"] = "group"
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_django_contrib_contenttypes_models_contenttype(**kwargs):
    defaults = {}
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_registry(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["id"] = "id"
    defaults.update(**kwargs)
    if "created_by" not in defaults:
        defaults["created_by"] = create_django_contrib_auth_models_user()
    return Registry.objects.create(**defaults)


def create_item(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["url"] = "url"
    defaults["img_url"] = "img_url"
    defaults["id"] = "id"
    defaults["description"] = "description"
    defaults.update(**kwargs)
    if "created_by" not in defaults:
        defaults["created_by"] = create_django_contrib_auth_models_user()
    return Item.objects.create(**defaults)


def create_registryitem(**kwargs):
    defaults = {}
    defaults["name"] = "name"
    defaults["bought_by"] = "bought_by"
    defaults["message"] = "message"
    defaults["bought"] = "bought"
    defaults["price_from_vendor"] = "price_from_vendor"
    defaults["price_display"] = "price_display"
    defaults["vendor"] = "vendor"
    defaults.update(**kwargs)
    if "registry" not in defaults:
        defaults["registry"] = create_registry()
    if "item" not in defaults:
        defaults["item"] = create_item()
    return RegistryItem.objects.create(**defaults)


class RegistryViewTest(unittest.TestCase):
    '''
    Tests for Registry
    '''
    def setUp(self):
        self.client = Client()

    def test_list_registry(self):
        url = reverse('registry_registry_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_registry(self):
        url = reverse('registry_registry_create')
        data = {
            "name": "name",
            "id": "id",
            "created_by": create_django_contrib_auth_models_user().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_registry(self):
        registry = create_registry()
        url = reverse('registry_registry_detail', args=[registry.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_registry(self):
        registry = create_registry()
        data = {
            "name": "name",
            "id": "id",
            "created_by": create_django_contrib_auth_models_user().pk,
        }
        url = reverse('registry_registry_update', args=[registry.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class ItemViewTest(unittest.TestCase):
    '''
    Tests for Item
    '''
    def setUp(self):
        self.client = Client()

    def test_list_item(self):
        url = reverse('registry_item_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_item(self):
        url = reverse('registry_item_create')
        data = {
            "name": "name",
            "url": "url",
            "img_url": "img_url",
            "id": "id",
            "description": "description",
            "created_by": create_django_contrib_auth_models_user().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_item(self):
        item = create_item()
        url = reverse('registry_item_detail', args=[item.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_item(self):
        item = create_item()
        data = {
            "name": "name",
            "url": "url",
            "img_url": "img_url",
            "id": "id",
            "description": "description",
            "created_by": create_django_contrib_auth_models_user().pk,
        }
        url = reverse('registry_item_update', args=[item.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


class RegistryItemViewTest(unittest.TestCase):
    '''
    Tests for RegistryItem
    '''
    def setUp(self):
        self.client = Client()

    def test_list_registryitem(self):
        url = reverse('registry_registryitem_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_registryitem(self):
        url = reverse('registry_registryitem_create')
        data = {
            "name": "name",
            "bought_by": "bought_by",
            "message": "message",
            "bought": "bought",
            "price_from_vendor": "price_from_vendor",
            "price_display": "price_display",
            "vendor": "vendor",
            "registry": create_registry().pk,
            "item": create_item().pk,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)

    def test_detail_registryitem(self):
        registryitem = create_registryitem()
        url = reverse('registry_registryitem_detail', args=[registryitem.slug,])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_registryitem(self):
        registryitem = create_registryitem()
        data = {
            "name": "name",
            "bought_by": "bought_by",
            "message": "message",
            "bought": "bought",
            "price_from_vendor": "price_from_vendor",
            "price_display": "price_display",
            "vendor": "vendor",
            "registry": create_registry().pk,
            "item": create_item().pk,
        }
        url = reverse('registry_registryitem_update', args=[registryitem.slug,])
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)


