from django import forms
from .models import Registry, Item, RegistryItem
from django.forms import Textarea


class RegistryForm(forms.ModelForm):
    class Meta:
        model = Registry
        fields = ['name', 'event_date', 'event_description']
        # exclude = ['created_by', 'id']
        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control"}),
            'event_date' : forms.DateInput(attrs={'class':'datepicker form-control'}),
            'event_description' :  Textarea(attrs={'cols': 80, 'rows': 10, 'class':"form-control"}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'url', 'img_url', 'id', 'description', 'created_by']


class RegistryItemForm(forms.ModelForm):
    class Meta:
        model = RegistryItem
        fields = ['name', 'bought_by', 'message', 'bought', 'price_from_vendor', 'price_display', 'vendor', 'registry', 'item']


