import json
import datetime
from datetime import timezone
import operator
import xml.etree.ElementTree as ET
import hashlib
import base64
import os
import uuid

from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView
from django.views.generic.edit import FormView
from .models import Registry, Item, RegistryItem, RegistryItemPaid, Transaction, Category
from .forms import RegistryForm, ItemForm, RegistryItemForm, RegistryItemBuyForm, CheckoutForm, RegistryItemPaidForm, ShopAddForm, ShopAddItemForm, CategoryForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, reverse

from django.db.models import Q
from functools import reduce

from carton.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string

from collections import OrderedDict
from django.db import IntegrityError
from decimal import Decimal

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import Context
from smtplib import SMTPException

from urllib.parse import urlparse

from django.conf import settings

SHOP_PK=2

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
        # registry = Registry.objects.get(pk=pk)
        try:
            registry = Registry.objects.get(pk=pk)
        except Registry.DoesNotExist:
            raise Http404

        if not (registry.created_by.id == request.user.id or request.user.is_superuser): 
            if "/registry/registry/detail/" in request.path:
                path_split = request.path.split("/")
                return redirect('registry_public_detail', pk=path_split[4])
            else:
                raise Http404
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

# check if partner stor
def is_partner_store(item_url):
    partner_stores = settings.PARTNER_STORES
    parsed_uri = urlparse( item_url )
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    print(domain)

    if any(domain in store for store in partner_stores):
        print("true!")
        return True
    else:
        print("false")
        return False



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

@method_decorator(login_required(login_url='index'), name='dispatch')
class RegistryListView(ListView):
    model = Registry

@method_decorator(login_required(login_url='index'), name='dispatch')
class RegistryCreateView(CreateView):
    model = Registry
    form_class = RegistryForm
    template_name = 'registry/registry_add.html'
    # success_url = '/home'

    def get_success_url(self):
        return reverse('registry_registry_detail',args=(self.object.id,))+"?initial=1"

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = self.request.user
            obj.save()

            email = self.request.user.email
            try:
                email_params = { 
                    'username': self.request.user 
                     }

                plaintext = render_to_string('registry/create_registry_email.txt', email_params)
                htmly     = render_to_string('registry/create_registry_email.html', email_params)

                subject, from_email, to = 'Baby Set Go', 'info@babysetgo.ph', email

                send_mail(
                    subject,
                    plaintext,
                    from_email,
                    [email,'info@babysetgo.ph', 'issarufinasenga@gmail.com', 'issa@babysetgo.ph'],
                    fail_silently=False,
                    html_message=htmly
                )
            except SMTPException as e:
                print(e.__cause__)
                error_msg = "E-mail sending error."

        return super(RegistryCreateView, self).form_valid(form)

@method_decorator(must_be_yours, name='dispatch')
class RegistryDetailView(DetailView):
    template_name = 'registry/registry.html'
    model = Registry

    def get(self,request,**kwargs):
        pk = kwargs["pk"]
        context = {}

        if pk == "0":
            raise Http404

        try:
            registry = Registry.objects.get(pk=pk)
        except registry.models.DoesNotExist:
            raise Http404

        # redirect if shop
        if registry.is_shop:
            return redirect('shop_pk',pk=pk)
        
        context = { 'pk': pk,
                    'object': registry}

        return render(request, self.template_name, context)

def check_valid_reservations(registry_id):
    if registry_id is None:
        return False

    registry_items = RegistryItem.objects.filter(registry=registry_id)
    for item in registry_items:
        # check if more than 24 hours
        registryItemPaid = RegistryItemPaid.objects.filter(registry_item=item, last_updated__lte=datetime.datetime.now(timezone.utc)-datetime.timedelta(days=2), paid=False)
        for item_paid in registryItemPaid:
            item_paid.reserved = False
            item_paid.save()
            registryItem = item_paid.registry_item
            if registryItem.quantity_bought-item_paid.quantity >= 0:
                registryItem.quantity_bought -= item_paid.quantity
                registryItem.save()

    return True

class RegistryDetailPublicView(DetailView):
    template_name = 'registry/registry_public.html'
    model = Registry

    def get(self,request,**kwargs):
        pk = kwargs["pk"]
        context = {}

        if pk == "0":
            raise Http404

        form = RegistryItemBuyForm()
        buy_form = RegistryItemPaidForm()
        # registry = Registry.objects.get(pk=pk)
        try:
            registry = Registry.objects.get(pk=pk)
        except Registry.DoesNotExist:
            raise Http404
        
        check_valid_reservations(registry.id)

        context = { 'form': form,
                    'buy_form': buy_form,
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
                (reduce(operator.and_,
                       (Q(name__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(name_father__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(name_mother__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(name_baby__icontains=q) for q in query_list))
                ) & (Q(is_shop=False))
                ).values()

        for p in result:
            print(p)

        return HttpResponse(json.dumps(list(result),default=datetime_handler), content_type="application/json")

@method_decorator(must_be_yours, name='dispatch')
class RegistryUpdateView(UpdateView):
    template_name = 'registry/registry_update.html'
    model = Registry
    form_class = RegistryForm

    def get_success_url(self):
        return reverse('registry_registry_detail',args=(self.object.id,))

@method_decorator(login_required(login_url='index'), name='dispatch')
class ItemListView(ListView):
    model = Item

@method_decorator(login_required(login_url='index'), name='dispatch')
class ItemCreateView(CreateView):
    model = Item
    form_class = ItemForm

@method_decorator(login_required(login_url='index'), name='dispatch')
class ItemDetailView(DetailView):
    model = Item

@method_decorator(login_required(login_url='index'), name='dispatch')
class ItemUpdateView(UpdateView):
    model = Item
    form_class = ItemForm

@method_decorator(login_required(login_url='index'), name='dispatch')
class RegistryItemListView(ListView):
    model = RegistryItem

@method_decorator(login_required(login_url='index'), name='dispatch')
class RegistryItemCreateView(CreateView):
    model = RegistryItem
    form_class = RegistryItemForm

@method_decorator(login_required(login_url='index'), name='dispatch')
class RegistryItemDetailView(DetailView):
    model = RegistryItem

@method_decorator(login_required(login_url='index'), name='dispatch')
class RegistryItemUpdateView(UpdateView):
    model = RegistryItem
    form_class = RegistryItemForm
    template_name = 'registry/registryitem_update.html'

    def get_success_url(self):
        view_name = 'registry_registry_detail'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse(view_name, kwargs={'pk': self.object.registry.id})

class RegistryItemSearch(DetailView):
    def post(self, request, **kwargs):
        print(request.POST.get('item_id'))
        query = request.POST.get('item_id')

        result = 0

        if query:
            query_result = RegistryItem.objects.get(pk=query)
            if query_result.quantity < query_result.quantity_bought:
                result = 1

        return HttpResponse(json.dumps(result,default=datetime_handler), content_type="application/json")

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
        registry.delete()
        # registryItem = RegistryItem.objects.get(pk=item_id)

        # registryItem.delete()

        # context = { 'object': registry }

        return redirect('home')

def add(request):
    cart = Cart(request.session)
    pk = int(request.GET.get('item_id'))

    registryItem = RegistryItem.objects.get(pk=pk)
    # check if item already in Cart before adding. If yes, replace quantity rather than add
    if registryItem in cart.products:
        cart._items_dict[pk].quantity = request.GET.get('item_qty')
    else:
        cart.add(registryItem, price=registryItem.price_from_vendor, quantity=request.GET.get('item_qty'))

    #reserve item
    # 1. increment qty_bought to reserve
    #registryItem.quantity_bought+=1
    #registryItem.save()
    # 2. set reserved status
    # 3. 

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
            cart.remove(registryItem)
            # if request.POST.get('delete_qty') is not None:
            #     delete_qty = int(request.POST.get('delete_qty'))
            #     ctr = 0
            #     while ctr < delete_qty:
            #         cart.remove_single(registryItem)
            #         # registryItem.quantity_bought-=1
            #         # registryItem.save()
            #         ctr += 1
        return render(request, 'registry/show_cart.html')

def compute_delivery_fee(item):
    delivery_fee = 0
    if(is_partner_store(item.product.item_url)):
        delivery_fee_ref = settings.DELIVERY_FEE_REF_PARTNER_STORE
    else:
        delivery_fee_ref = settings.DELIVERY_FEE_REF

    if(item.product.price_from_vendor <= settings.PRICE_REF[0]):
        delivery_fee += delivery_fee_ref[0]
    elif(item.product.price_from_vendor <= settings.PRICE_REF[1]):
        delivery_fee += delivery_fee_ref[1]
    elif(item.product.price_from_vendor <= settings.PRICE_REF[2]):
        delivery_fee += delivery_fee_ref[2]
    else:
        delivery_fee += delivery_fee_ref[3]
    return delivery_fee

@csrf_exempt
def checkout(request):
    if request.method == "GET":
        form = RegistryItemPaidForm()
        cart = Cart(request.session)
        #delivery_fee = (cart.total * Decimal('0.12')).quantize(Decimal('0.01'))
        delivery_fee = 0

        # get Cart products
        cart = Cart(request.session)

        if cart.is_empty:
            error_msg = "You have no items in your gift basket!"
        else:
            error_msg = ""
            for productItem in cart.items:
                #if(is_partner_store(productItem.product.item_url)):
                #    delivery_fee += settings.DELIVERY_FEE_PARTNER_STORE
                #else:
                #    delivery_fee += settings.DELIVERY_FEE
                #print(compute_delivery_fee(productItem))
                delivery_fee += compute_delivery_fee(productItem)

        cart_total = cart.total + delivery_fee
                
        context = { 'form' : form,
                    'delivery_fee' : delivery_fee,
                    'empty_cart' : cart.is_empty,
                    'cart_total' : cart_total,
                    'error_msg' : error_msg
                }

        return render(request, 'registry/checkout.html', context)

    elif request.method == "POST":
        form = RegistryItemPaidForm()
        cart = Cart(request.session)
        delivery_fee = 0
        context = {}

        # get Cart products
        cart = Cart(request.session)

        if cart.is_empty:
            error_msg = "You have no items in your gift basket!"
        else:
            error_msg = ""
            for productItem in cart.items:
                #if(is_partner_store(productItem.product.item_url)):
                #    delivery_fee += settings.DELIVERY_FEE_PARTNER_STORE
                #else:
                #    delivery_fee += settings.DELIVERY_FEE
                delivery_fee += compute_delivery_fee(productItem)

        cart_total = cart.total + delivery_fee

        # get POST params
        name = request.POST.get('name')
        message = request.POST.get('message')
        email = request.POST.get('email')
        tel_no = request.POST.get('tel_no')
        mobile = request.POST.get('mobile')

        giver_info = {
            'name' : name,
            'message' : message,
            'email' : email,
            'tel_no' : tel_no,
            'mobile' : mobile,
        }

        context = {'giver_info': giver_info}
        request.session['giver_name'] = name
        request.session['giver_message'] = message
        request.session['giver_email'] = email
        request.session['giver_mobile'] = mobile
        request.session['giver_tel_no'] = tel_no

        for productItem in cart.items:
            # create new RegistryItemPaid for each product
            
            # update quantity
            #if (productItem.product.quantity_bought + productItem.quantity) < productItem.product.quantity:
            # productItem.product.quantity_bought += productItem.quantity
            # productItem.product.save()
            #else:
            #    raise ValueError("Product quantity to be bought is greater than available quantity")

            registryItemPaid = RegistryItemPaid.objects.filter(
                email=email,
                registry_item=productItem.product).first()

            if(registryItemPaid is not None):
                # duplicate entry
                error_msg = "It seems you have already bought " + productItem.product.name + " using the e-mail you have provided. You should have received an e-mail notification of the said transaction. If not, please contact us for assistance."
                    
                context = { 'form' : form,
                            'delivery_fee' : delivery_fee,
                            'empty_cart' : cart.is_empty,
                            'cart_total' : cart_total,
                            'error_msg' : error_msg
                            }

                return render(request, 'registry/checkout.html', context)

        return redirect('payment')

@csrf_exempt
def payment(request):
    if request.method == "GET":
        context = {}
        given_info = None
        # get Cart products
        cart = Cart(request.session)
        # delivery_fee = (cart.total * Decimal('0.12')).quantize(Decimal('0.01'))
        convenience_fee = (cart.total * Decimal('0.044')).quantize(Decimal('0.01'))+Decimal(15.00)
        delivery_fee = 0

        if request.session.get('giver_name', None) is None:
            return redirect('show-cart')

        if cart.is_empty:
            error_msg = "You have no items in your gift basket!"
            context = { 'error_msg' : error_msg }
            return redirect('show-cart')
        else:
            error_msg = ""
            for productItem in cart.items:
                #if(is_partner_store(productItem.product.item_url)):
                #    delivery_fee += settings.DELIVERY_FEE_PARTNER_STORE
                #else:
                #    delivery_fee += settings.DELIVERY_FEE 
                delivery_fee += compute_delivery_fee(productItem)

        cart_total = cart.total + delivery_fee
        cart_total_2 = cart.total + delivery_fee + convenience_fee

        # get user info from session
        name = request.session['giver_name']
        message = request.session['giver_message']
        email = request.session['giver_email']
        tel_no = request.session['giver_tel_no']
        mobile = request.session['giver_mobile']

        giver_info = {
            'name' : name,
            'message' : message,
            'email' : email,
            'tel_no' : tel_no,
            'mobile' : mobile,
        }

        context = {
            'giver_info': giver_info,
            'delivery_fee' : delivery_fee,
            'empty_cart' : cart.is_empty,
            'cart_total' : cart_total,
            'cart_total_2' : cart_total_2,
            'error_msg' : error_msg,
            'convenience_fee' : convenience_fee
            }

        return render(request, 'registry/payment.html', context)

    if request.method == "POST":
        context = {}

        if request.session.get('giver_name', None) is None:
            return redirect('show-cart')

        # get POST params
        name = request.POST.get('name')
        message = request.POST.get('message')
        email = request.POST.get('email')
        tel_no = request.POST.get('tel_no')
        mobile = request.POST.get('mobile')
        payment_option = request.POST.get('payment_option')
        amount = request.POST.get('amount')

        # get Cart products
        cart = Cart(request.session)
        convenience_fee = (cart.total * Decimal('0.044')).quantize(Decimal('0.01'))+Decimal(15.00)

        # delivery_fee = (cart.total * Decimal('0.12')).quantize(Decimal('0.01'))
        paid = False
        delivery_fee = 0
        for productItem in cart.items:
            #if(is_partner_store(productItem.product.item_url)):
            #    delivery_fee += settings.DELIVERY_FEE_PARTNER_STORE
            #else:
            #    delivery_fee += settings.DELIVERY_FEE
        
            delivery_fee += compute_delivery_fee(productItem)

        if payment_option == '1':
            amount_paid = 0
            date_paid = None
            cart_total = cart.total + delivery_fee
        elif payment_option == '2':
            amount_paid = amount
            date_paid = datetime.datetime.now()
            cart_total = cart.total + delivery_fee
            paid = True
            #cart_total = cart.total + delivery_fee + convenience_fee


        # create transaction object
        transaction = Transaction.objects.create(
                name=name,
                message=message,
                email=email,
                tel_no=tel_no,
                mobile=mobile,
                total_amount = cart_total,
                total_amount_paid = amount_paid,
                date_paid = date_paid,
            )

        transaction_reference = str(transaction.id)

        for productItem in cart.items:
            # create new RegistryItemPaid for each product
            try:
                # update quantity
                #if (productItem.product.quantity_bought + productItem.quantity) < productItem.product.quantity:
                productItem.product.quantity_bought += productItem.quantity
                productItem.product.bought = True
                productItem.product.bought_by = name
                productItem.product.save()
                #else:
                #    raise ValueError("Product quantity to be bought is greater than available quantity")

                registryItemPaid = RegistryItemPaid.objects.create(
                    name=name,
                    message=message,
                    email=email,
                    tel_no=tel_no,
                    mobile=mobile,
                    reserved=True,
                    paid=paid,
                    quantity=productItem.quantity,
                    registry_item=productItem.product,
                    transaction = transaction)

            except IntegrityError as e:
                print(e.__cause__)
                transaction.delete()
                
                if e.args[0] == 1062:
                    # duplicate entry
                    error_msg = "It seems you have already bought " + productItem.product.name + " using the e-mail you have provided. You should have received an e-mail notification of the said transaction. If not, please contact us for assistance."
                else:
                    error_msg = "There was an error processing your transaction. Please contact us for assistance."
                
                context = { 'error_msg' : error_msg,
                            'delivery_fee' : delivery_fee,
                            'cart_total' : cart_total }

                return render(request, 'registry/payment.html', context)

            except ValueError as e:
                print(e.__cause__)
                error_msg = "ValueError"
                context = { 'error_msg' : error_msg }
                
                return render(request, 'registry/payment.html', context)

        # assume transaction is complete if code is here

        # send email
        try:
            email_params = { 
                'username': name, 
                'transaction_reference': transaction_reference,
                'cart_items': cart.items,
                'delivery_fee': delivery_fee,
                'cart_total': cart_total }

            if payment_option == '1':
                plaintext = render_to_string('registry/transaction_email.txt', email_params)
                htmly     = render_to_string('registry/transaction_email.html', email_params)
            elif payment_option == '2':
                plaintext = render_to_string('registry/transaction_email_card.txt', email_params)
                htmly     = render_to_string('registry/transaction_email_card.html', email_params)

            subject, from_email, to = 'Baby Set Go Purchase', 'info@babysetgo.ph', email

            send_mail(
                subject,
                plaintext,
                from_email,
                [email,'info@babysetgo.ph', 'issarufinasenga@gmail.com', 'issa@babysetgo.ph'],
                fail_silently=False,
                html_message=htmly
            )
        except SMTPException as e:
            print(e.__cause__)
            error_msg = "E-mail sending error."
            context = { 'error_msg' : error_msg }
                
            #return render(request, 'registry/payment.html', context)
            return redirect('payment-done',pk=3)


        # temporarily bank transfer only
        context = {'payment_option' : payment_option }

        # delete from session if transaction is complete
        if request.session['giver_name']:
            del request.session['giver_name']
        if request.session['giver_message']:
            del request.session['giver_message']
        if request.session['giver_email']:
            del request.session['giver_email']
        if request.session['giver_tel_no']:
            del request.session['giver_tel_no']
        if request.session['giver_mobile']:
            del request.session['giver_mobile']

        # clear cart if transaction is complete
        cart.clear()

        #return render(request, 'registry/payment-done.html', context)
        return redirect('payment-done',pk=payment_option)

def payment_done(request, pk):
    context = {'payment_option' : pk }
    return render(request, 'registry/payment-done.html', context)

class ShopView(DetailView):
    """
    View for rendering a basic Lists templates used in the starter
    """
    template_name = 'registry/shop.html'
    model = Registry

    def get(self,request):
        context = {}
        try:
            registry = Registry.objects.filter(is_shop=True)
        except Registry.DoesNotExist:
            registry = None

        context = {'object_list': registry}

        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='index'), name='dispatch')
class ShopCreateView(CreateView):
    model = Registry
    form_class = ShopAddForm
    template_name = 'registry/shop_add.html'

    def post(self,request,**kwargs):
        if request.FILES is None or request.POST is None:
            raise Http404

        registry = Registry.objects.create(
                name=request.POST.get('name'),
                event_description='',
                event_date='2000-01-01',
                event_venue='',
                name_baby='',
                name_mother='',
                name_father='',
                address=request.POST.get('address'),
                delivered_where='',
                birth_or_due_date='2000-01-01',
                is_shop=True,
                img_shop=request.FILES['img_shop'],
                created_by=self.request.user,
            )
        return redirect('shop')

class ShopDetailView(DetailView):
    template_name = 'registry/shop_detail.html'
    model = Registry

    def get(self,request,**kwargs):
        pk = kwargs["pk"]
        if pk is None:
            pk=SHOP_PK

        context = {}
        form = RegistryItemBuyForm()
        # registry = Registry.objects.get(pk=pk)
        
        if(request.user.is_authenticated()):
            my_registries = Registry.objects.filter(created_by=request.user)
            print(str(my_registries))
        else:
            print("Anonymous")

        try:
            registry = Registry.objects.get(pk=pk)
        except Registry.DoesNotExist:
            raise Http404
        
        context = { 'form': form,
                    'object': registry,
                    'my_registries': my_registries
                    }

        return render(request, self.template_name, context)


# def get_file_path(instance, filename):
#     ext = filename.split('.')[-1]
#     filename = "%s.%s" % (uuid.uuid4(), ext)
#     return os.path.join('uploads/logos', filename)

@method_decorator(staff_member_required, name='dispatch')
class ShopItemCreateView(CreateView):
    model = RegistryItem
    form_class = ShopAddItemForm
    template_name = 'registry/shop_add.html'

    def get(self,request,**kwargs):
        pk = kwargs["pk"]
        if pk is None:
            pk=SHOP_PK

        context = {}
        form = ShopAddItemForm()
        # registry = Registry.objects.get(pk=pk)
        
        try:
            registry = Registry.objects.get(pk=pk)
        except Registry.DoesNotExist:
            raise Http404
        
        context = { 'form': form,
                    'shop_name': registry.name,
                    }

        return render(request, self.template_name, context)

    def post(self,request,**kwargs):
        pk = kwargs["pk"]
        if request.FILES is None or request.POST is None:
            raise Http404

        # file_uploaded = request.FILES['img_shop']
        # ext = file_uploaded.name.split('.')[-1]
        # filename = "%s.%s" % (uuid.uuid4(), ext)
        # file_upload_path = settings.UPLOAD_ROOT + os.path.join('uploads/shop', filename)
        # media_path = "media/uploads/shop/%s" % (filename)

        # with open(file_upload_path, 'wb+') as destination:
        #     for chunk in file_uploaded.chunks():
        #         destination.write(chunk)

        try:
            shop_registry = Registry.objects.get(pk=pk)
        except Registry.DoesNotExist:
            raise Http404

        # shop_registry = Registry.objects.get(pk=pk)

        registryItem = RegistryItem.objects.create(
                name=request.POST.get('name'),
                price_from_vendor=request.POST.get('price_from_vendor'),
                price_display=request.POST.get('price_from_vendor'),
                item_url="None",
                #img_url=settings.MEDIA_URL + os.path.join('uploads/shop', filename),
                img_url="None",
                bought=0,
                quantity=request.POST.get('quantity'),
                registry_id=shop_registry.id,
                quantity_bought=0,
                item_notes="None",
                message=request.POST.get('message'),
                from_partner_store=1,
                img_shop=request.FILES['img_shop'],
            )
        return redirect('shop')

@method_decorator(staff_member_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'registry/category_add.html'
    success_url = '/shop/add/category'

@csrf_exempt
def reserve_item(request):
    if request.method == "GET":
        form = RegistryItemPaidForm()

        # get POST params
        name = request.GET.get('name')
        message = request.GET.get('message')
        email = request.GET.get('email')
        qty = request.GET.get('quantity')
        mobile = request.GET.get('mobile')
        item_id = request.GET.get('item_id')

        giver_info = {
            'name' : name,
            'message' : message,
            'email' : email,
            'mobile' : mobile,
            'qty': qty,
        }

        context = {'giver_info': giver_info}

        registry_item = RegistryItem.objects.get(pk=item_id);

        if registry_item is None:
        # duplicate entry
            error_msg = "Item does not exist"
                    
            context = { 'giver_info' : giver_info,
                        'error_msg' : error_msg
                        }
            return render(request, 'registry/after_buy.html', context)

        registryItemPaid = RegistryItemPaid.objects.filter(
                    email=email,
                    registry_item=registry_item,
                    reserved=1,
                ).first()

        if(registryItemPaid is not None):
        # duplicate entry
            error_msg = "It seems you have already reserved " + registry_item.name + " using the e-mail you have provided. You should have received an e-mail notification of the said transaction. If not, please contact us for assistance."
                
            context = { 'giver_info': giver_info,
                        'error_msg' : error_msg,
                        'item_url': registryItemPaid.registry_item.item_url,
                        'address': registryItemPaid.registry_item.registry.address,
                        'event_name': registryItemPaid.registry_item.registry.name,
                        'owner': registryItemPaid.registry_item.registry.name_mother,
                        }

            return render(request, 'registry/after_buy.html', context)

        try:
        # update quantity
        #if (productItem.product.quantity_bought + productItem.quantity) < productItem.product.quantity:
            registry_item.quantity_bought += int(qty)
            registry_item.bought = True
            registry_item.bought_by = name
            #else:
        #    raise ValueError("Product quantity to be bought is greater than available quantity")

            transaction = Transaction.objects.create(
                name=name,
                message=message,
                email=email,
                # tel_no=tel_no,
                mobile=mobile,
                total_amount = 0,
                total_amount_paid = 0,
                date_paid = None,
            )

            registryItemPaid = RegistryItemPaid.objects.create(
                name=name,
                message=message,
                email=email,
                mobile=mobile,
                reserved=True,
                paid=False,
                quantity=qty,
                registry_item=registry_item,
                transaction=transaction,
                )

        except IntegrityError as e:
            print(e.__cause__)
                
            if e.args[0] == 1062:
                    # duplicate entry
                error_msg = "It seems you have already reserved " + registry_item.name + " using the e-mail you have provided. You should have received an e-mail notification of the said transaction. If not, please contact us for assistance."
                registryItemPaid = RegistryItemPaid.objects.get(email=email,registry_item=registry_item)
                if registryItemPaid.reserved == False:
                    registryItemPaid.reserved = True
                    registryItemPaid.transaction = transaction
                    registryItemPaid.save()
            else:
                error_msg = "There was an error processing your transaction. Please contact us for assistance."
                context = { 'error_msg' : error_msg }
                return render(request, 'registry/after_buy.html', context)

        except ValueError as e:
            print(e.__cause__)
            error_msg = "ValueError"
            context = { 'error_msg' : error_msg }
                
            return render(request, 'registry/after_buy.html', context)

        # assume transaction is complete if code is here
        registry_item.save()
        # send email
        try:
            email_params = { 
                'username': name, 
                'transaction_reference': str(transaction.id),
                'item': registryItemPaid,
                'host': request.get_host(),
                }

            plaintext = render_to_string('registry/transaction_email_2.txt', email_params)
            htmly     = render_to_string('registry/transaction_email_2.html', email_params)

            subject, from_email, to = 'Baby Set Go Purchase', 'info@babysetgo.ph', email

            send_mail(
                subject,
                plaintext,
                from_email,
                [email,'info@babysetgo.ph', 'issarufinasenga@gmail.com', 'issa@babysetgo.ph'],
                fail_silently=False,
                html_message=htmly
            )
        except SMTPException as e:
            print(e.__cause__)
            error_msg = "E-mail sending error."
            context = { 'error_msg' : error_msg }
            transaction.delete()
            registryItemPaid.delete()
                
            #return render(request, 'registry/payment.html', context)
            # return redirect('payment-done',pk=3)

        context = { 'giver_info': giver_info,
                    'item_url': registryItemPaid.registry_item.item_url,
                    'address': registryItemPaid.registry_item.registry.address,
                    'event_name': registryItemPaid.registry_item.registry.name,
                    'owner': registryItemPaid.registry_item.registry.name_mother,
                     }
        return render(request, 'registry/after_buy.html', context)

def confirm_transaction(request, transaction_reference=None):
    context = { 'transaction_reference' : transaction_reference}
    registryItemPaid = RegistryItemPaid.objects.filter(
                    transaction=transaction_reference,
                ).first()
    print(registryItemPaid.name)

    if registryItemPaid is None:
        error_msg = "Transaction does not exist"
        context = { 'error_msg' : error_msg }
        return render(request, 'registry/after_confirmation.html', context)

    if registryItemPaid.reserved is False:
        error_msg = "Your reservation has expired. Please reserve again."
        context = { 'error_msg' : error_msg }
        return render(request, 'registry/after_confirmation.html', context)

    if registryItemPaid.paid:
        error_msg = "Transaction already confirmed"
        context = { 'error_msg' : error_msg }
        return render(request, 'registry/after_confirmation.html', context)

    transaction = Transaction.objects.get(pk=transaction_reference)
    transaction.date_paid = datetime.datetime.now()
    transaction.save()
    registryItemPaid.paid = True
    registryItemPaid.save()


    return render(request, 'registry/after_confirmation.html', context)

def cancel_transaction(request, transaction_reference=None):
    if request.method == "GET":
        context = { 'transaction_reference' : transaction_reference}
        registryItemPaid = RegistryItemPaid.objects.filter(
                        transaction=transaction_reference,
                    ).first()
        print(registryItemPaid.name)

        if registryItemPaid is None:
            error_msg = "Transaction does not exist"
            context = { 'error_msg' : error_msg }
            return render(request, 'registry/after_cancellation.html', context)

        if registryItemPaid.reserved == False:
            error_msg = "Transaction already cancelled"
            context = { 'error_msg' : error_msg }
            return render(request, 'registry/after_cancellation.html', context)

        registryItemPaid.paid = False
        registryItemPaid.reserved = False
        registryItemPaid.save()

        registryItem = registryItemPaid.registry_item
        if registryItem.quantity_bought-registryItemPaid.quantity >= 0:
            registryItem.quantity_bought -= registryItemPaid.quantity
            registryItem.save()

        return render(request, 'registry/after_cancellation.html', context)
    elif request.method == "POST":
        context = { 'transaction_reference' : transaction_reference, }
        registryItemPaid = RegistryItemPaid.objects.filter(
                        transaction=transaction_reference,
                    ).first()
        print(registryItemPaid.name)

        if registryItemPaid is None:
            error_msg = "Transaction does not exist"
            context = { 'transaction_reference' : transaction_reference,
                        'status' : 'failed',
                        'message' : error_msg }
            return HttpResponse(json.dumps(list(context),default=datetime_handler), content_type="application/json")

        registryItemPaid.paid = False
        registryItemPaid.reserved = False
        registryItemPaid.save()

        registryItem = registryItemPaid.registry_item
        registryItem.quantity_bought -= registryItemPaid.quantity
        registryItem.save()

        context = { 'transaction_reference' : transaction_reference,
                        'status' : 'success',
                        'message' : 'cancellation success' }

        return HttpResponse(json.dumps(list(context),default=datetime_handler), content_type="application/json")

