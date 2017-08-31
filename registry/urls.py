from django.conf.urls import url, include
# from rest_framework import routers
# import api
from . import views

# router = routers.DefaultRouter()
# router.register(r'registry', api.RegistryViewSet)
# router.register(r'item', api.ItemViewSet)
# router.register(r'registryitem', api.RegistryItemViewSet)


urlpatterns = (
    # urls for Django Rest Framework API
    # url(r'^api/v1/', include(router.urls)),
    # url(r'^home/$', views.HomeView.as_view(), name='home'),
    url(r'^registry/add/$', views.RegistryCreateView.as_view(), name='registry_create'),
    url(r'^public/registry/detail/(?P<pk>\S+)/$', views.RegistryDetailPublicView.as_view(), name='registry_public_detail'),
    url(r'^public/registry/search/', views.RegistrySearchView.as_view(), name='registry_search'),
    url(r'^public/registry/search/(?P<query>\S+)/$', views.RegistrySearchView.as_view(), name='registry_search'),
)

urlpatterns += (
    url(r'^add-cart/$', views.add, name='add-cart'),
    url(r'^show-cart/$', views.show, name='show-cart'),
    url(r'^checkout/$', views.checkout, name='checkout-cart'),
    url(r'^payment/$', views.payment, name='payment'),
    url(r'^payment/done/$', views.payment, name='payment-done'),
)

urlpatterns += (
    # urls for Registry
    url(r'^registry/registry/$', views.RegistryListView.as_view(), name='registry_registry_list'),
    url(r'^registry/registry/create/$', views.RegistryCreateView.as_view(), name='registry_registry_create'),
    url(r'^registry/registry/detail/(?P<pk>\S+)/$', views.RegistryDetailView.as_view(), name='registry_registry_detail'),
    url(r'^registry/registry/update/(?P<pk>\S+)/$', views.RegistryUpdateView.as_view(), name='registry_registry_update'),
    url(r'^registry/registry/delete/(?P<pk>\S+)/$', views.RegistryDeleteView.as_view(), name='registry_registry_delete'),
)

urlpatterns += (
    # urls for Item
    url(r'^registry/item/$', views.ItemListView.as_view(), name='registry_item_list'),
    url(r'^registry/item/create/$', views.ItemCreateView.as_view(), name='registry_item_create'),
    url(r'^registry/item/detail/(?P<pk>\S+)/$', views.ItemDetailView.as_view(), name='registry_item_detail'),
    url(r'^registry/item/update/(?P<pk>\S+)/$', views.ItemUpdateView.as_view(), name='registry_item_update'),
)

urlpatterns += (
    # urls for RegistryItem
    url(r'^registry/registryitem/$', views.RegistryItemListView.as_view(), name='registry_registryitem_list'),
    url(r'^registry/registryitem/create/$', views.RegistryItemCreateView.as_view(), name='registry_registryitem_create'),
    url(r'^registry/registryitem/detail/(?P<pk>\S+)/$', views.RegistryItemDetailView.as_view(), name='registry_registryitem_detail'),
    url(r'^registry/registryitem/update/(?P<pk>\S+)/$', views.RegistryItemUpdateView.as_view(), name='registry_registryitem_update'),
    url(r'^registry/registryitem/delete/(?P<pk>\S+)/$', views.RegistryItemDeleteView.as_view(), name='registry_registryitem_delete'),
)

