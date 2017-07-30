from django.views.generic import DetailView, ListView, UpdateView, CreateView, TemplateView
from django.views.generic.edit import FormView
from .models import Registry, Item, RegistryItem
from .forms import RegistryForm, ItemForm, RegistryItemForm, RegistryItemBuyForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from registry.forms import RegistryForm

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
