from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.sites.models import Site
from . import views
admin.autodiscover()
admin.site.unregister(Site)

urlpatterns = [
    url(r'^$', views.index, name='home'),

    #url(r'^list/(?P<condicion_slug>[a-zA-Z]+)/(?P<localidad_slug>[a-zA-Z]+)(?:/(?P<tipo_slug>[a-zA-Z]+))?/$', views.lista, name='lista'),

    url(r'^list/$', views.lista, name='lista'),

    url(r'^prop/(?P<tit_slug>[-\w]+)/$', views.propiedad_detalle, name='propiedad_detalle'),

    url(r'^servicios/', views.servicios, name='servicios'),

    url(r'^contacto/', views.contacto, name='contacto'),

    url(r'^admin/', include(admin.site.urls)),
]

if not settings.PRODUCCION:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]