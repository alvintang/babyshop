from django import forms
from .models import Registry, Item, RegistryItem
from django.forms import Textarea
from django.utils.translation import ugettext as _

class RegistryForm(forms.ModelForm):
    class Meta:
        model = Registry
        fields = ['name', 'event_date', 'event_description', 'event_venue', 'name_baby', 'name_mother', 'name_father', 'address', 'delivered_where', 'due_date', 'baby_birthdate']
        # exclude = ['created_by', 'id']
        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control"}),
            'event_date' : forms.DateInput(attrs={'class':'datepicker form-control'}),
            'event_description' :  Textarea(attrs={'cols': 80, 'rows': 10, 'class':"form-control"}),
            'event_venue' : forms.TextInput(attrs={'class': "form-control"}),
            'name_baby' : forms.TextInput(attrs={'class': "form-control"}),
            'name_mother' : forms.TextInput(attrs={'class': "form-control"}),
            'name_father' : forms.TextInput(attrs={'class': "form-control"}),
            'address' : forms.TextInput( attrs={'class': "form-control"}),
            'due_date' : forms.DateInput(attrs={'class':'datepicker form-control'}),
            'baby_birthdate' : forms.DateInput(attrs={'class':'datepicker form-control'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'url', 'img_url', 'id', 'description', 'created_by']


class RegistryItemForm(forms.ModelForm):
    class Meta:
        model = RegistryItem
        fields = ['name', 'price_from_vendor', 'price_display', 'item_url', 'img_url']
        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control"}),
            'price_display' : forms.NumberInput(attrs={'class': "form-control"}),
            'price_from_vendor' : forms.TextInput(attrs={'class': "form-control"}),
            'item_url' : forms.TextInput( attrs={'class': "form-control"}),
            'img_url' : forms.TextInput(attrs={'class':'form-control'}),
        }


class RegistryItemBuyForm(forms.Form):
  name = forms.CharField(label=_('Your Name'), required=True, max_length=50, 
                widget=forms.TextInput(attrs={'class': "form-control", 'id': 'name'}))
  item_qty = forms.IntegerField(label=_('Quantity'), required=True,
                widget=forms.NumberInput(attrs={'class': "form-control", 'id': 'item_qty'}))
  message = forms.CharField(label=_('Your Message'),required=False,  max_length=500, 
                widget=forms.Textarea(attrs={'class': "form-control", 'id':'message'}))
  item_id = forms.CharField(initial='',required=True,  max_length=200, 
                widget=forms.HiddenInput(attrs={'id': 'item_id'}))