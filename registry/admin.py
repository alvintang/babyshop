from django.contrib import admin
from django import forms
from .models import Registry, Item, RegistryItem, Transaction, RegistryItemPaid
from django.core import urlresolvers

class CustomModelChoiceField(forms.ModelChoiceField):
     def label_from_instance(self, obj):
         return "%s - %s" % (obj.id, obj.name)

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
    registry = CustomModelChoiceField(queryset=Registry.objects.all()) 
    class Meta:
        model = RegistryItem
        fields = '__all__'

class RegistryItemAdmin(admin.ModelAdmin):
    form = RegistryItemAdminForm
    list_display = ['name', 'created', 'last_updated', 'get_registry', 'price_from_vendor', 'item_url', 'img_url', 'item_notes', 'quantity', 'quantity_bought', 'registry', 'registry_name', 'registry_id']
    readonly_fields = ['name', 'created', 'last_updated', 'price_display', 'item_url', 'img_url', 'registry_name', 'registry_id']
    search_fields = ['registry__name']

    def get_registry(self,obj):
        link=urlresolvers.reverse("admin:registry_registry_change", args=[obj.registry.id]) #model name has to be lowercase
        return u'<a href="%s">%s</a>' % (link,obj.registry.name)
    get_registry.allow_tags=True

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

class RegistryItemPaidAdminForm(forms.ModelForm):
    registry_item = CustomModelChoiceField(queryset=RegistryItem.objects.all()) 
    transaction = CustomModelChoiceField(queryset=Transaction.objects.all()) 
    class Meta:
        model = RegistryItemPaid
        fields = '__all__'

class RegistryItemPaidAdmin(admin.ModelAdmin):
    form = RegistryItemPaidAdminForm
    list_display = ['name', 'created', 'last_updated', 'reserved', 'paid', 'quantity', 'get_registry_item', 'get_transaction']
    readonly_fields = ['name', 'created', 'last_updated']

    def get_registry_item(self,obj):
        link=urlresolvers.reverse("admin:registry_registryitem_change", args=[obj.registry_item.id]) #model name has to be lowercase
        return u'<a href="%s">%s</a>' % (link,obj.registry_item.name)
    get_registry_item.allow_tags=True
    def get_transaction(self, obj):
        link=urlresolvers.reverse("admin:registry_transaction_change", args=[obj.transaction.id]) #model name has to be lowercase
        return u'<a href="%s">%s</a>' % (link,obj.transaction.name)
    get_transaction.allow_tags=True


admin.site.register(RegistryItemPaid, RegistryItemPaidAdmin)


