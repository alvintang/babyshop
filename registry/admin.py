from django.contrib import admin
from django import forms
from .models import Registry, Item, RegistryItem

class RegistryAdminForm(forms.ModelForm):

    class Meta:
        model = Registry
        fields = '__all__'


class RegistryAdmin(admin.ModelAdmin):
    form = RegistryAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'id']
    readonly_fields = ['name', 'slug', 'created', 'last_updated', 'id']

admin.site.register(Registry, RegistryAdmin)


class ItemAdminForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'


class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'url', 'img_url', 'id', 'description']
    readonly_fields = ['name', 'slug', 'created', 'last_updated', 'url', 'img_url', 'id', 'description']

admin.site.register(Item, ItemAdmin)


class RegistryItemAdminForm(forms.ModelForm):

    class Meta:
        model = RegistryItem
        fields = '__all__'


class RegistryItemAdmin(admin.ModelAdmin):
    form = RegistryItemAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'bought_by', 'message', 'bought', 'price_from_vendor', 'price_display', 'item_url']
    readonly_fields = ['name', 'slug', 'created', 'last_updated', 'bought_by', 'message', 'bought', 'price_from_vendor', 'price_display', 'item_url']

admin.site.register(RegistryItem, RegistryItemAdmin)


