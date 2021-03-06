from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.i18n import JavaScriptCatalog

from . import views
from django.views.defaults import server_error as server_error_view

from django.views.static import serve

urlpatterns = [
    url(r'^', include('users.urls')),
    url(r'^', include('registry.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
    #url(r'^proto/$', views.IndexView.as_view(), name='index'),
    url(r'^500/$', server_error_view, name='error500'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^lists/$', views.ListsView.as_view(), name='lists'),
    url(r'^home/$', views.ListsView.as_view(), name='home'),
    url(r'^panels/$', views.PanelsView.as_view(), name='panels'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/$', views.BlogDetailView.as_view(), name='blog_detail'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^babysetgo/', include('babysetgo.urls')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy-policy'),
    url(r'^external/add/$', views.ExternalView.as_view(), name='external'),
    url(r'^external/add/item/$', views.AddToList.as_view(), name='external_item'),
    url(r'^articles/$', views.ComingSoonView.as_view(), name='articles'),
    url(r'^faqs/$', views.FaqsView.as_view(), name='faqs'),
    url(r'^samples/$', views.ComingSoonView.as_view(), name='samples'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
