from django.contrib import admin
from django import forms
from .models import Registry, Item, RegistryItem, Transaction

class RegistryAdminForm(forms.ModelForm):

    class Meta:
        model = Registry
        fields = '__all__'


class RegistryAdmin(admin.ModelAdmin):
    form = RegistryAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'id', 'event_description', 'event_date', 'event_venue', 'name_baby', 'name_mother', 'name_father', 'address', 'delivered_where', 'birth_or_due_date']
    readonly_fields = ['name', 'slug', 'created', 'last_updated', 'id', 'event_description', 'event_date', 'event_venue', 'name_baby', 'name_mother', 'name_father', 'address', 'delivered_where', 'birth_or_due_date']

admin.site.register(Registry, RegistryAdmin)


class ItemAdminForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = '__all__'


class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'url', 'img_url', 'id', 'description']
    readonly_fields = ['name', 'slug', 'created', 'last_updated', 'url', 'img_url', 'id', 'description']

# admin.site.register(Item, ItemAdmin)


class RegistryItemAdminForm(forms.ModelForm):

    class Meta:
        model = RegistryItem
        fields = '__all__'


class RegistryItemAdmin(admin.ModelAdmin):
    form = RegistryItemAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'bought_by', 'message', 'bought', 'price_from_vendor', 'price_display', 'item_url', 'img_url', 'item_notes', 'quantity', 'quantity_bought']
    readonly_fields = ['name', 'slug', 'created', 'last_updated', 'bought_by', 'message', 'bought', 'price_from_vendor', 'price_display', 'item_url', 'img_url', 'item_notes', 'quantity', 'quantity_bought']

admin.site.register(RegistryItem, RegistryItemAdmin)

class TransactionAdminForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    list_display = ['name', 'slug', 'created', 'last_updated', 'message', 'email', 'tel_no', 'mobile', 'total_amount', 'total_amount_paid', 'date_paid', 'id']
    readonly_fields = ['name', 'slug', 'created', 'last_updated', 'message', 'email', 'tel_no', 'mobile', 'total_amount', 'id']

admin.site.register(Transaction, TransactionAdmin)


