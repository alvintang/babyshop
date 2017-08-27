from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView
from django.views.generic.edit import FormView
from .models import Registry, Item, RegistryItem
from .forms import RegistryForm, ItemForm, RegistryItemForm, RegistryItemBuyForm, CheckoutForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from registry.forms import RegistryForm

import json
import datetime
import operator

from django.db.models import Q
from functools import reduce

from carton.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

import xml.etree.ElementTree as ET
import hashlib
import base64
from collections import OrderedDict

def datetime_handler(x):
    if hasattr(x, 'isoformat'):
        return x.isoformat()
    raise TypeError("Unknown type")

#Custom decorator
def must_be_yours(func):
    def check_and_call(request, *args, **kwargs):
        # user = request.user
        # print("user_id:"+user.id)
        # print(kwargs)
        pk = kwargs["pk"]
        registry = Registry.objects.get(pk=pk)
        if not (registry.created_by.id == request.user.id): 
            return HttpResponse("It is not yours ! You are not permitted !",
                        content_type="application/json", status=403)
        return func(request, *args, **kwargs)
    return check_and_call

# get client IP
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

User = get_user_model()

@method_decorator(login_required(login_url='index'), name='dispatch')
class HomeView(TemplateView):
    """
    Home view
    """
    template_name = 'registry/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['authenticated'] = self.request.user.is_authenticated()
        if context['authenticated']:
            context['user_detail'] = User.objects.get(username=self.request.user)
        return context

class RegistryView(FormView):
    template_name = 'base/contact.html'
    form_class = RegistryForm
    success_url = '/home'

    def form_valid(self, form):
        return super(RegistryView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super(RegistryListView, self).get_context_data(**kwargs)
        ctx['RegistryItem'] = RegistryItem.objects.all().filter(User=self.request.user)
        return ctx


class RegistryListView(ListView):
    model = Registry

class RegistryCreateView(CreateView):
    model = Registry
    form_class = RegistryForm
    template_name = 'registry/registry_add.html'
    success_url = '/home'

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = self.request.user
            obj.save()
        return super(RegistryCreateView, self).form_valid(form)

@method_decorator(must_be_yours, name='dispatch')
class RegistryDetailView(DetailView):
    template_name = 'registry/registry.html'
    model = Registry

    def get(self,request,**kwargs):
        pk = kwargs["pk"]
        context = {}
        registry = Registry.objects.get(pk=pk)
        
        context = { 'pk': pk,
                    'object': registry}

        return render(request, self.template_name, context)

class RegistryDetailPublicView(DetailView):
    template_name = 'registry/registry_public.html'
    model = Registry

    def get(self,request,**kwargs):
        pk = kwargs["pk"]
        context = {}
        form = RegistryItemBuyForm()
        registry = Registry.objects.get(pk=pk)
        
        context = { 'form': form,
                    'object': registry}

        return render(request, self.template_name, context)

class RegistrySearchView(DetailView):
    template_name = 'registry/registry_search.html'
    model = Registry

    def get(self,request,**kwargs):
        context = {}

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        print(request.POST.get('query'))

        query = request.POST.get('query')

        result = {}

        if query:
            query_list = query.split()
            result = Registry.objects.all().filter(
                reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(name_father__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(name_mother__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(name_baby__icontains=q) for q in query_list))
            ).values()

        for p in result:
            print(p)

        return HttpResponse(json.dumps(list(result),default=datetime_handler), content_type="application/json")


class RegistryUpdateView(UpdateView):
    template_name = 'registry/registry_update.html'
    model = Registry
    form_class = RegistryForm


class ItemListView(ListView):
    model = Item


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm


class ItemDetailView(DetailView):
    model = Item


class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm


class RegistryItemListView(ListView):
    model = RegistryItem


class RegistryItemCreateView(CreateView):
    model = RegistryItem
    form_class = RegistryItemForm


class RegistryItemDetailView(DetailView):
    model = RegistryItem


class RegistryItemUpdateView(UpdateView):
    model = RegistryItem
    form_class = RegistryItemForm
    template_name = 'registry/registryitem_update.html'

    def get_success_url(self):
        view_name = 'registry_registry_detail'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse(view_name, kwargs={'pk': self.object.id})

@method_decorator(must_be_yours, name='dispatch')
class RegistryItemDeleteView(UpdateView):
    template_name = 'registry/registry.html'
    model = Registry

    def get(self,request,**kwargs):
        context = {}
        pk = kwargs["pk"]
        item_id = request.GET.get('item_id');
        registry = Registry.objects.get(pk=pk)
        registryItem = RegistryItem.objects.get(pk=item_id)

        registryItem.delete()

        context = { 'object': registry }

        return render(request, self.template_name, context)

@method_decorator(must_be_yours, name='dispatch')
class RegistryDeleteView(UpdateView):
    template_name = 'registry/home.html'
    model = Registry

    def get(self,request,**kwargs):
        context = {}
        pk = kwargs["pk"]
        item_id = request.GET.get('item_id');
        registry = Registry.objects.get(pk=pk)
        # registryItem = RegistryItem.objects.get(pk=item_id)

        # registryItem.delete()

        # context = { 'object': registry }

        return redirect('home')

def add(request):
    cart = Cart(request.session)
    pk = int(request.GET.get('item_id'))

    registryItem = RegistryItem.objects.get(pk=pk)
    cart.add(registryItem, price=registryItem.price_from_vendor, quantity=request.GET.get('item_qty'))
    view_name = 'registry_registry_detail'
        # No need for reverse_lazy here, because it's called inside the method
    return redirect(request.GET.get('next'))

def show(request):
    cart = Cart(request.session)
    if request.method == "GET":
        return render(request, 'registry/show_cart.html')
    elif request.method == "POST":
        # print(request.POST.get('delete_id'))
        if request.POST.get('delete_id') is not None:
            delete_id = int(request.POST.get('delete_id'))
            registryItem = RegistryItem.objects.get(pk=delete_id)
            if request.POST.get('delete_qty') is not None:
                delete_qty = int(request.POST.get('delete_qty'))
                ctr = 0
                while ctr < delete_qty:
                    cart.remove_single(registryItem)
                    ctr += 1
        return render(request, 'registry/show_cart.html')

@csrf_exempt
def checkout(request):
    if request.method == "GET":
        form = CheckoutForm()
        context = { 'form' : form }
        return render(request, 'registry/checkout.html', context)
    elif request.method == "POST":
        # Paynamics integration
        # get XML parameters
        _mid = "000000020817E0B9C58E"
        _request_id = get_random_string(length=14)
        _ipaddress = "192.168.10.1"
        _noturl = request.get_host() + reverse('payment-done')
        _resurl = request.get_host() + reverse('payment-done')
        _cancelurl = request.get_host() + reverse('payment-done')
        _fname = str(request.POST.get('first_name'))
        _mname = str(request.POST.get('middle_name'))
        _lname = str(request.POST.get('last_name'))
        _addr1 = str(request.POST.get('address1'))
        _addr2 = str(request.POST.get('address2'))
        _city = str(request.POST.get('city'))
        _state = str(request.POST.get('state'))
        _country = str(request.POST.get('country'))
        _zip = str(request.POST.get('zipcode'))
        _sec3d = "try3d"
        _email = str(request.POST.get('email_add'))
        _phone = str(request.POST.get('phone'))
        _mobile = str(request.POST.get('mobile'))
        _clientip = str(get_client_ip(request))
        _amount = '2.00'
        _currency = 'PHP'
        forSignature = _mid + _request_id + _ipaddress + _noturl + _resurl + _fname + _lname + _mname + _addr1 + _addr2 + _city + _state + _country + _zip + _email + _phone + _clientip + _amount + _currency + _sec3d
        cert = "E3F103CDDF8B76E1645461950C288BE5"
        forSignature = forSignature+cert
        _signature = hashlib.sha512(forSignature.encode('utf-8')).hexdigest()

        post_params = OrderedDict()
        post_params['First Name'] = str(request.POST.get('first_name'))
        post_params['Middle Name'] = str(request.POST.get('middle_name'))
        post_params['Last Name'] = str(request.POST.get('last_name'))
        post_params['Address 1'] = str(request.POST.get('address1'))
        post_params['Address 2'] = str(request.POST.get('address2'))
        post_params['City'] = str(request.POST.get('city'))
        post_params['Province/Region'] = str(request.POST.get('state'))
        post_params['Country'] = str(request.POST.get('country'))
        post_params['Zip Code'] = str(request.POST.get('zipcode'))
        post_params['E-mail'] = str(request.POST.get('email_add'))
        post_params['Phone'] = str(request.POST.get('phone'))
        post_params['Mobile'] = str(request.POST.get('mobile'))

        # build a tree structure
        rootRequest = ET.Element("Request")

        orders = ET.SubElement(rootRequest, "orders")

        items = ET.SubElement(orders, "items") #item list header
        
        item = ET.SubElement(items, "Items") #specific item list
        itemname = ET.SubElement(item, "itemname")
        itemname.text = "Item 1"
        itemqty = ET.SubElement(item, "quantity")
        itemqty.text = "1"
        itemamount = ET.SubElement(item, "amount")
        itemamount.text = "1.00"

        item = ET.SubElement(items, "Items") #specific item list
        itemname = ET.SubElement(item, "itemname")
        itemname.text = "Shipping Fee"
        itemqty = ET.SubElement(item, "quantity")
        itemqty.text = "1"
        itemamount = ET.SubElement(item, "amount")
        itemamount.text = "1.00"

        mid = ET.SubElement(rootRequest, "mid")
        mid.text = _mid

        request_id = ET.SubElement(rootRequest, "request_id")
        request_id.text = _request_id

        ip_address = ET.SubElement(rootRequest, "ip_address")
        ip_address.text = _ipaddress

        notification_url = ET.SubElement(rootRequest, "notification_url")
        notification_url.text = _noturl

        response_url = ET.SubElement(rootRequest, "response_url")
        response_url.text = _resurl

        cancel_url = ET.SubElement(rootRequest, "cancel_url")
        cancel_url.text = _cancelurl

        mtac_url = ET.SubElement(rootRequest, "mtac_url")
        mtac_url.text = ''

        descriptor_note = ET.SubElement(rootRequest, "descriptor_note")
        descriptor_note.text = ''

        fname = ET.SubElement(rootRequest, "fname")
        fname.text = _fname

        lname = ET.SubElement(rootRequest, "lname")
        lname.text = _lname

        mname = ET.SubElement(rootRequest, "mname")
        mname.text = _mname

        address1 = ET.SubElement(rootRequest, "address1")
        address1.text = _addr1

        address2 = ET.SubElement(rootRequest, "address2")
        address2.text = _addr2

        city = ET.SubElement(rootRequest, "city")
        city.text = _city

        state = ET.SubElement(rootRequest, "state")
        state.text = _state

        country = ET.SubElement(rootRequest, "country")
        country.text = _country

        zipcode = ET.SubElement(rootRequest, "zip")
        zipcode.text = _zip

        secure3d = ET.SubElement(rootRequest, "secure3d")
        secure3d.text = "try3d"

        trxtype = ET.SubElement(rootRequest, "trxtype")
        trxtype.text = "sale"

        email = ET.SubElement(rootRequest, "email")
        email.text = _email

        phone = ET.SubElement(rootRequest, "phone")
        phone.text = _phone

        mobile = ET.SubElement(rootRequest, "mobile")
        mobile.text = _mobile

        client_ip = ET.SubElement(rootRequest, "client_ip")
        client_ip.text = _clientip

        amount = ET.SubElement(rootRequest, "amount")
        amount.text = _amount

        currency = ET.SubElement(rootRequest, "currency")
        currency.text = _currency

        mlogo_url = ET.SubElement(rootRequest, "mlogo_url")
        mlogo_url.text = ''

        pmethod = ET.SubElement(rootRequest, "pmethod")
        pmethod.text = ''

        signature = ET.SubElement(rootRequest, "signature")
        signature.text = _signature

        # wrap it in an ElementTree instance, and save as XML
        # tree = ET.ElementTree(root)
        # tree.write("page.xhtml")
        xml_str = ET.tostring(rootRequest)
        b64_str = base64.b64encode(xml_str)
        print(b64_str)

        # return HttpResponse(ET.tostring(rootRequest), content_type='text/xml');
        context = { 'b64_str' : b64_str,
                    'post_params' : post_params}
        return render(request, 'registry/confirm-payment.html', context)

@csrf_exempt
def payment(request):

    return HttpResponse("ok!");