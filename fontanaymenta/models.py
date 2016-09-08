#encoding:utf-8
import datetime
from django.utils import timezone
from django.conf import settings
from django.template.defaultfilters import slugify
from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete, post_save
from django.contrib.contenttypes.fields import GenericRelation
from PIL import Image

from sorl.thumbnail import ImageField, get_thumbnail, delete
from ckeditor.fields import RichTextField

class Slider(models.Model):
    file = models.FileField(upload_to=settings.SLIDER_UPLOAD_PATH, help_text='2200x800')
    titulo = models.CharField(max_length=90)
    link = models.URLField(blank=True, null=True)
    precio = models.CharField(max_length=15, blank=True, null=True)
    descripcion = models.TextField(blank=True,null=True)
    mostrar_info = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)

    # ------  COLUMNAS CUSTOM ADMIN  ---- #
    def admin_image(self):
        if self.file:
            content_type = ContentType.objects.get_for_model(self.__class__)
            return '<a target="_blank" href="%s"><img style="max-width: 120px; max-height:95px" src="%s"/></a>' \
                   % (urlresolvers.reverse('admin:' + content_type.app_label + '_' + content_type.model + '_change', args=(self.id,)),self.file.url)
        else:
            return '(Sin imagen)'
    admin_image.short_description = 'Img'
    admin_image.allow_tags = True


class Localidad(models.Model):
    titulo = models.CharField(max_length=90, db_index=True)
    slug = models.SlugField(max_length=90,editable=False,unique=True)

    def __unicode__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Localidad, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Localidades'


class Servicio(models.Model):
    titulo = models.CharField(max_length=90, db_index=True)

    def __unicode__(self):
        return self.titulo


class Tipo(models.Model):
    titulo = models.CharField(max_length=90, db_index=True)
    slug = models.SlugField(max_length=90,editable=False,unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Tipo, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.titulo


class PropiedadImagen(models.Model):
    imagen = ImageField(upload_to=settings.IMAGE_UPLOAD_PATH)
    propiedad = models.ForeignKey('Propiedad')

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imágenes'

    def __unicode__(self):
        return self.imagen.name


class Propiedad(models.Model):
    titulo = models.CharField(max_length=90)
    tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
    localidad = models.ForeignKey(Localidad, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=200)
    descripcion = RichTextField()
    precio = models.IntegerField(blank=True, null=True)

    CONDICIONES = (
        (1, 'Venta'),
        (2, 'Alquiler'),
    )
    condicion = models.IntegerField(choices=CONDICIONES)
    servicios = models.ManyToManyField(Servicio, through='PropiedadServicio')

    fecha = models.DateTimeField(auto_now_add=True)
    fecha_ultima_edicion = models.DateTimeField(auto_now=True)
    destacado = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    slug = models.SlugField(max_length=90,editable=False,unique=True)

    def __unicode__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.titulo)
        super(Propiedad, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Propiedades'

class PropiedadServicio(models.Model):
    propiedad = models.ForeignKey(Propiedad)
    servicio = models.ForeignKey(Servicio)
    info = models.CharField(max_length=128)

    def __unicode__(self):
        return self.servicio.titulo


#---- SEÑALES ----#
'''
@receiver(post_save, sender=PropiedadImagen)
def resize_original(sender, instance, created, **kwargs):
    #Hace resize si la imagen se pasa de 800px tanto de ancho como alto
    if created:
        imagen = Image.open(instance.imagen.path)
        if (imagen.size[0] > 900 or imagen.size[1] > 900):
            ratio = float(imagen.size[0]) / float(imagen.size[1])
            if ratio > 1:
                target_size=(900, int(900/ratio))
            else:
                target_size=(int(900*ratio),900)
            imagen = imagen.resize((target_size), Image.ANTIALIAS)
            imagen.save(instance.imagen.path, optimize=True, quality=65, progressive=True)
        else:
            imagen.save(instance.imagen.path, optimize=True, quality=65, progressive=True)
        del imagen
'''