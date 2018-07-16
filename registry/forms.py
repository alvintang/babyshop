from django import forms
from .models import Registry, Item, RegistryItem, RegistryItemPaid, Category
from django.forms import Textarea
from django.utils.translation import ugettext as _
import uuid
import os

from crispy_forms import bootstrap, layout
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div

class RegistryForm(forms.ModelForm):
    class Meta:
        model = Registry
        fields = ['name', 'event_date', 'event_description', 'event_venue', 'name_baby', 'name_mother', 'name_father', 'address','img_shop']
        labels = {
          'name' : _('Registry Name'),
          'name_baby': _('Name of Baby'),
          'name_mother': _('Name of Mother'),
          'name_father': _('Name of Father'),
          'img_shop': _('Event Image'),
          'event_description': _('You may also write a short note to family and friends :)'),
          'address': _('Address'),
          # 'birth_or_due_date': _('Due Date/Baby Birthdate'),
        }
        # exclude = ['created_by', 'id']
        widgets = {
            'name' : forms.TextInput(attrs={'class': "baby-form-input col-sm-8"}),
            'event_date' : forms.DateTimeInput(attrs={'class':'baby-form-input-addon-group col-sm-12'}),
            'event_description' :  Textarea(attrs={'cols': 80, 'rows': 10, 'class':"baby-form-input col-sm-8"}),
            'event_venue' : forms.TextInput(attrs={'class': "baby-form-input col-sm-8"}),
            'name_baby' : forms.TextInput(attrs={'class': "baby-form-input col-sm-8"}),
            'name_mother' : forms.TextInput(attrs={'class': "baby-form-input col-sm-8", 'placeholder': "This name will be used for the delivery details"}),
            'name_father' : forms.TextInput(attrs={'class': "baby-form-input col-sm-8"}),
            'address' : forms.TextInput( attrs={'class': "baby-form-input col-sm-8", 'placeholder': "Gifts will be shipped to this address"}),
            'img_shop' : forms.FileInput( attrs={'class': "baby-form-file col-sm-8"}),
            # 'birth_or_due_date' : forms.DateInput(attrs={'class':'datepicker form-control', 'id': 'birth_or_due_date'}),
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
        fields = ['name', 'price_from_vendor', 'price_display', 'item_url', 'img_url', 'quantity', 'item_notes']
        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control"}),
            'price_display' : forms.NumberInput(attrs={'class': "form-control"}),
            'price_from_vendor' : forms.NumberInput(attrs={'class': "form-control"}),
            'item_url' : forms.TextInput( attrs={'class': "form-control"}),
            'img_url' : forms.TextInput(attrs={'class':'form-control'}),
            'item_notes' : forms.TextInput(attrs={'class':'form-control'}),
            'message' : forms.Textarea(attrs={'class': "form-control"}),
        }

class ShopAddForm(RegistryForm):
    class Meta:
        model = Registry
        fields = ['name', 'address','img_shop']
        labels = {
          'name': _('Shop Name'),
          'address': _('Shop Address'),
          'img_shop': _('Shop Logo'),
        }
        # exclude = ['created_by', 'id']
        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control"}),
            'address' : forms.TextInput( attrs={'class': "form-control"}),
        }

class ShopAddItemForm(RegistryItemForm):
    #item_img = forms.ImageField()

    def __init__(self, *args, **kwargs):
            super(ShopAddItemForm, self).__init__(*args, **kwargs)
            self.fields.pop('price_display')
            self.fields.pop('item_url')
            self.fields.pop('img_url')

    class Meta(RegistryItemForm.Meta):
      fields = RegistryItemForm.Meta.fields + ['message', 'img_shop','categories']
      #fields = RegistryItemForm.Meta.fields + ['message']
      #widgets = RegistryItemForm.Meta.widgets['message'] = forms.Textarea(attrs={'class': "form-control"})

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
        fields = ['name', 'message', 'email', 'mobile','quantity']
        labels = {
          'name' : 'Your Name',
          'message' : 'Message to Baby or Mommy',
        }
        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control"}),
            'message' : forms.Textarea(attrs={'class': "form-control"}),
            'email' : forms.EmailInput(attrs={'class': "form-control"}),
            'mobile' : forms.TextInput(attrs={'class': "form-control"}),
            'quantity': forms.NumberInput(attrs={'class': "form-control", 'id': 'item_qty'}),
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

class CategoryForm(forms.ModelForm):
  class Meta:
        model = Category
        fields = ['name', 'parent']
        labels = {
          'name' : 'Category Name',
          'parent' : 'Parent Category',
        }