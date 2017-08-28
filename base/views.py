from base.forms import ContactForm, AddToListForm
from base.logic import getImageList, getTitle, getPrice, getCurrency

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView

from django.views.decorators.clickjacking import xframe_options_exempt

from users.forms import LoginForm
from registry.models import Registry, RegistryItem

from bs4 import BeautifulSoup
import urllib, re

User = get_user_model()


class ComingSoonView(TemplateView):
    """
    Index view
    """
    template_name = 'base/index.html'
    form = LoginForm()

    def post(self, request):
        context = {}
        self.form = LoginForm(request.POST or None)

        if request.POST and self.form.is_valid():
            user_email = request.POST['email']
            user_password = request.POST['password']
            username = User.objects.get(email=user_email).username
            user = authenticate(username=username, password=user_password)
            auth_login(request, user)
            context['authenticated'] = request.user.is_authenticated()
            if context['authenticated']:
                context['username'] = request.user.username
                return redirect('home')

        context.update({'login_form': self.form,
                        'login_failed': 'true'})

        return render(request, self.template_name, context)

class IndexView(TemplateView):
    """
    Index view
    """
    template_name = 'baby/index.html'
    form = LoginForm()

    def get(self,request):
        context = {}
        self.form = LoginForm(request.POST or None)

        if request.user.is_authenticated():
            return redirect('home')
        
        context.update({'login_form': self.form,
                        'login_failed': 'false'})

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        self.form = LoginForm(request.POST or None)

        if request.POST and self.form.is_valid():
            user_email = request.POST['email']
            user_password = request.POST['password']
            username = User.objects.get(email=user_email).username
            user = authenticate(username=username, password=user_password)
            auth_login(request, user)
            context['authenticated'] = request.user.is_authenticated()
            if context['authenticated']:
                context['username'] = request.user.username
                return redirect('home')

        context.update({'login_form': self.form,
                        'login_failed': 'true'})

        return render(request, self.template_name, context)

class ContactView(FormView):
    template_name = 'base/contact.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        send_mail(
            'Contact - {} - {}'.format(form.cleaned_data.get('contact_email'),
                                       form.cleaned_data.get('contact_name')),
            form.cleaned_data.get('content'),
            settings.EMAIL_FROM,
            [settings.EMAIL_TO],
            fail_silently=False,
        )
        return super(ContactView, self).form_valid(form)


@method_decorator(login_required(login_url='index'), name='dispatch')
class ListsView(ListView):
    """
    View for rendering a basic Lists templates used in the starter
    """
    template_name = 'registry/list.html'
    model = Registry

    def get(self,request):
        context = {}
        try:
            registry = Registry.objects.filter(created_by_id=request.user)
        except Registry.DoesNotExist:
            registry = None

        context = {'object_list': registry}

        return render(request, self.template_name, context)

@method_decorator(xframe_options_exempt, name='dispatch')
@method_decorator(login_required(login_url='index'), name='dispatch')
class ExternalView(ListView):
    """
    View for rendering a basic Lists templates used in the starter
    """
    template_name = 'baby/modal.html'

    def get(self,request):
        url = request.GET.get('url','')
        reg_id = request.GET.get('reg_id','')

        # get images from url
        # source,headers = urllib.request.urlretrieve(url)
        with urllib.request.urlopen(url) as response:
            source = response.read().decode('utf-8')

        # list to store URLs
        img_list = []

        # run BeautifulSoup on source
        soup = BeautifulSoup(source)
        
        getImageList(soup, img_list)

        title = getTitle(soup)

        price = getPrice(soup)

        currency = getCurrency(soup)

        form = AddToListForm(initial={'item_name': title, 'item_qty': '1', 'item_price': price, 'item_url': url, 'reg_id':reg_id})
        # print(img_list)
        context = {'links':img_list, 'form': form}

        return render(request, self.template_name, context)

    def post(self, request):
        template = 'baby/after_add.html'
        context = {}
        print(request.POST)

        item_name = request.POST.get('item_name')
        item_qty = int(request.POST.get('item_qty'))
        item_price = float(request.POST.get('item_price').replace(',',''))
        item_url = request.POST.get('item_url')
        item_img = request.POST.get('item_img')
        item_notes = request.POST.get('item_notes')
        reg_id = request.POST.get('reg_id')
        registry = Registry.objects.get(pk=reg_id)

        reg_item = RegistryItem.objects.create(name=item_name, quantity=item_qty, bought_by='', message='', price_from_vendor=item_price, price_display=item_price*1.12, item_url=item_url, registry=registry, img_url=item_img, item_notes=item_notes, bought=False, quantity_bought=0)
        reg_item.save()

        return render(request, template, context)

@method_decorator(login_required(login_url='index'), name='dispatch')
class AddToList(TemplateView):
    template_name = 'baby/modal.html'
    def post(self, request):
        context = {}
        print(request)
        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='index'), name='dispatch')
class PanelsView(TemplateView):
    """
    View for rendering a basic Lists templates used in the starter
    """
    template_name = 'base/panels.html'


class BlogDetailView(TemplateView):
    """
    Main blog detail view
    """
    template_name = 'base/blog_detail.html'


class PrivacyPolicyView(TemplateView):
    template_name = 'base/privacy-policy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyPolicyView, self).get_context_data(**kwargs)
        return context
