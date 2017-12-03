from django import forms
from django.utils.translation import ugettext as _
from django.core.validators import MinValueValidator
from decimal import Decimal


class ContactForm(forms.Form):
    contact_name = forms.CharField(label=_('Your name'), required=True,
                                   widget=forms.TextInput(attrs={'class': "form-control"}))
    contact_email = forms.EmailField(label=_('Your email'), required=True,
                                     widget=forms.EmailInput(attrs={'class': "form-control"}))
    content = forms.CharField(
        label=_("Leave us your message"),
        required=True,
        widget=forms.Textarea(attrs={'class': "form-control"})
    )

class AddToListForm(forms.Form):
  item_name = forms.CharField(label=_('Item'), required=True, max_length=50, 
                widget=forms.TextInput(attrs={'class': "form-control", 'id': 'item_name'}))
  item_price = forms.DecimalField(label=_('Price'), required=True, decimal_places=2, max_digits=12,  min_value=0,
                widget=forms.NumberInput(attrs={'class': "form-control", 'id': 'item_price'}))
  item_qty = forms.IntegerField(label=_('Quantity'), required=True, min_value=0,
                widget=forms.NumberInput(attrs={'class': "form-control", 'id': 'item_qty'}))
  item_notes = forms.CharField(label=_('Additional Notes'),required=False,  max_length=200, 
                widget=forms.Textarea(attrs={'class': "form-control"}))
  item_img = forms.CharField(initial='',required=True,  max_length=200, 
                widget=forms.HiddenInput(attrs={'id': 'item_img'}))
  item_url = forms.CharField(initial='',required=True,  max_length=200, 
                widget=forms.HiddenInput(attrs={'id': 'item_url'}))
  reg_id = forms.CharField(initial='',required=True,  max_length=200, 
                widget=forms.HiddenInput(attrs={'id': 'reg_id'}))