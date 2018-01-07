from django import forms
from .models import Registry, Item, RegistryItem, RegistryItemPaid
from django.forms import Textarea
from django.utils.translation import ugettext as _
import uuid
import os

class RegistryForm(forms.ModelForm):
    class Meta:
        model = Registry
        fields = ['name', 'event_date', 'event_description', 'event_venue', 'name_baby', 'name_mother', 'name_father', 'address', 'delivered_where', 'birth_or_due_date']
        labels = {
          'name_baby': _('Name of Baby'),
          'name_mother': _('Name of Mother'),
          'name_father': _('Name of Father'),
          'birth_or_due_date': _('Due Date/Baby Birthdate'),
        }
        # exclude = ['created_by', 'id']
        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control"}),
            'event_date' : forms.DateTimeInput(attrs={'class':'form-control'}),
            'event_description' :  Textarea(attrs={'cols': 80, 'rows': 10, 'class':"form-control"}),
            'event_venue' : forms.TextInput(attrs={'class': "form-control"}),
            'name_baby' : forms.TextInput(attrs={'class': "form-control"}),
            'name_mother' : forms.TextInput(attrs={'class': "form-control"}),
            'name_father' : forms.TextInput(attrs={'class': "form-control"}),
            'address' : forms.TextInput( attrs={'class': "form-control"}),
            'birth_or_due_date' : forms.DateInput(attrs={'class':'datepicker form-control', 'id': 'birth_or_due_date'}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'url', 'img_url', 'id', 'description', 'created_by']


class RegistryItemForm(forms.ModelForm):
    class Meta:
        model = RegistryItem
        labels = {
          "price_from_vendor" : "Price",
          "message" : "Description"
          }
        fields = ['name', 'price_from_vendor', 'price_display', 'item_url', 'img_url', 'quantity']
        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control"}),
            'price_display' : forms.NumberInput(attrs={'class': "form-control"}),
            'price_from_vendor' : forms.NumberInput(attrs={'class': "form-control"}),
            'item_url' : forms.TextInput( attrs={'class': "form-control"}),
            'img_url' : forms.TextInput(attrs={'class':'form-control'}),
            'message' : forms.TextInput(attrs={'class': "form-control"}),
        }

class ShopAddForm(RegistryItemForm):
    #item_img = forms.ImageField()

    def __init__(self, *args, **kwargs):
            super(ShopAddForm, self).__init__(*args, **kwargs)
            self.fields.pop('price_display')
            self.fields.pop('item_url')
            self.fields.pop('img_url')

    class Meta(RegistryItemForm.Meta):
      fields = RegistryItemForm.Meta.fields + ['message', 'img_shop']
      #fields = RegistryItemForm.Meta.fields + ['message']
      # widgets = RegistryItemForm.Meta.widgets['message'] = forms.TextInput(attrs={'class': "form-control"}) }

class RegistryItemBuyForm(forms.Form):
  name = forms.CharField(label=_('Your Name'), required=True, max_length=50, 
                widget=forms.HiddenInput(attrs={'class': "form-control", 'id': 'name'}))
  item_qty = forms.IntegerField(label=_('Quantity'), required=True,
                widget=forms.NumberInput(attrs={'class': "form-control", 'id': 'item_qty'}))
  # message = forms.CharField(label=_('Your Message'),required=False,  max_length=500, 
  #               widget=forms.Textarea(attrs={'class': "form-control", 'id':'message'}))
  item_id = forms.CharField(initial='',required=True,  max_length=200, 
                widget=forms.HiddenInput(attrs={'id': 'item_id'}))
  item_price = forms.CharField(initial='',required=True,  max_length=200, 
                widget=forms.HiddenInput(attrs={'id': 'item_price'}))

class RegistryItemPaidForm(forms.ModelForm):
    class Meta:
        model = RegistryItemPaid
        fields = ['name', 'message', 'email', 'tel_no', 'mobile']
        labels = {
          'name' : 'Your Name',
          'message' : 'Message to Baby or Mommy',
        }
        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control"}),
            'message' : forms.Textarea(attrs={'class': "form-control"}),
            'email' : forms.EmailInput(attrs={'class': "form-control"}),
            'tel_no' : forms.TextInput(attrs={'class': "form-control"}),
            'mobile' : forms.TextInput(attrs={'class': "form-control"}),
        }

class CheckoutForm(forms.Form):
  first_name = forms.CharField(label=_('First Name'), required=True, max_length=50, 
                widget=forms.TextInput(attrs={'class': "form-control", 'id': 'fname'}))
  middle_name = forms.CharField(label=_('Middle Name'), required=False, max_length=50, 
                widget=forms.TextInput(attrs={'class': "form-control", 'id': 'mname'}))
  last_name = forms.CharField(label=_('Last Name'), required=True, max_length=50, 
                widget=forms.TextInput(attrs={'class': "form-control", 'id': 'lname'}))
  email_add = forms.CharField(label=_('Email Address'), required=True, max_length=50,widget=forms.EmailInput(attrs={'class': "form-control", 'id': 'email_add'}))
  mobile = forms.CharField(label=_('Mobile Number'), required=False, max_length=15, 
                widget=forms.TextInput(attrs={'class': "form-control", 'id': 'mobile'}))
  phone = forms.CharField(label=_('Phone Number'), required=False, max_length=12, 
                widget=forms.TextInput(attrs={'class': "form-control", 'id': 'phone'}))
  address1 = forms.CharField(label=_('Address 1'), required=True, max_length=300, widget=forms.TextInput(attrs={'class': "form-control", 'id': 'addr1'}))
  address2 = forms.CharField(label=_('Address 2'), required=True, max_length=300, widget=forms.TextInput(attrs={'class': "form-control", 'id': 'addr2'}))
  city = forms.CharField(label=_('City'), required=True, max_length=100, widget=forms.TextInput(attrs={'class': "form-control", 'id': 'city'}))
  state = forms.CharField(label=_('Province/Region'), required=True, max_length=100, widget=forms.TextInput(attrs={'class': "form-control", 'id': 'state'}))
  country = forms.CharField(label=_('Country'), required=True, max_length=100, widget=forms.TextInput(attrs={'class': "form-control", 'id': 'country'}))
  zipcode = forms.CharField(label=_('Zip Code'), required=True, max_length=8, widget=forms.TextInput(attrs={'class': "form-control", 'id': 'zipcode'}))
