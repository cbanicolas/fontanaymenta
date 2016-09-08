#encoding:utf-8
from django.contrib import admin
from django.forms import forms, CharField
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Slider, Localidad, Servicio, Propiedad, Tipo, PropiedadImagen

class SliderAdmin(admin.ModelAdmin):
    list_display = ['admin_image','titulo','descripcion','precio','mostrar_info','visible']
    list_editable = ['titulo','descripcion','precio','mostrar_info','visible']
    search_fields = ['titulo','descripcion']

class TipoAdmin(admin.ModelAdmin):
    list_display = ['id','titulo']
    list_editable = ['titulo']
    list_filter = ['titulo']
    search_fields = ['titulo']

class LocalidadAdmin(admin.ModelAdmin):
    list_display = ['id','titulo']
    list_editable = ['titulo']
    list_filter = ['titulo']
    search_fields = ['titulo']

class ServicioAdmin(admin.ModelAdmin):
    list_display = ['id','titulo']
    list_editable = ['titulo']
    list_filter = ['titulo']
    search_fields = ['titulo']

#class PropiedadImagenAdmin(AdminImageMixin, admin.ModelAdmin):
#    pass

class PropiedadImagenInline(AdminImageMixin, admin.TabularInline):
    model = PropiedadImagen
class PropiedadServiciotInline(admin.TabularInline):
    model = Propiedad.servicios.through
class PropiedadAdmin(admin.ModelAdmin):
    list_display = ['titulo','condicion','tipo','destacado','visible','fecha']
    list_editable = ['condicion','tipo','destacado','visible']
    list_filter = ['fecha']
    date_hierarchy = 'fecha'
    search_fields = ['titulo','descripcion']
    inlines = [PropiedadServiciotInline,PropiedadImagenInline, ]

admin.site.register(Slider,SliderAdmin)
admin.site.register(Localidad,LocalidadAdmin)
admin.site.register(Servicio,ServicioAdmin)
admin.site.register(Propiedad,PropiedadAdmin)
admin.site.register(Tipo,TipoAdmin)
#admin.site.register(PropiedadImagen,PropiedadImagenAdmin)