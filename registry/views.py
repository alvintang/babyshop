from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView
from django.views.generic.edit import FormView
from .models import Registry, Item, RegistryItem
from .forms import RegistryForm, ItemForm, RegistryItemForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from registry.forms import RegistryForm

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


class RegistryDetailView(DetailView):
    template_name = 'registry/registry.html'
    model = Registry


class RegistryUpdateView(UpdateView):
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

