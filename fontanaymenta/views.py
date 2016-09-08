#encoding:utf-8
from django.utils import timezone
from django.http import HttpResponse,HttpResponseRedirect, Http404, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404, redirect, render
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse

from .utils import enviar_mail
from .models import Slider, Tipo, PropiedadImagen, PropiedadServicio, Localidad, Propiedad


def index(request):
    context = {
        'destacados' : Propiedad.objects.filter(destacado=True,visible=True).order_by('-id')[:6],
        'propieadades' : Propiedad.objects.filter(destacado=False,visible=True).order_by('-id')[:6],
        'sliders' : Slider.objects.filter(visible=True).order_by('-id'),
        'tipos' : Tipo.objects.order_by('-id'),
        'localidades' : Localidad.objects.order_by('-id'),
        'navbar_active_inicio': 'active',
    }
    return render_to_response('inicio.html',context, context_instance=RequestContext(request))


def lista(request):

    condicion = request.GET.get('condicion',None)
    localidad = request.GET.get('localidad',None)
    tipo =      request.GET.get('tipo',None)

    #Preparo el title y el h1
    titulo = {}
    if tipo:
        titulo['tipo'] = Tipo.objects.get(id=tipo)
    if localidad:
        titulo['localidad'] = Localidad.objects.get(id=localidad)
    if condicion == '1':
        titulo['condicion'] = 'Venta'
    elif condicion == '2':
        titulo['condicion'] = 'Alquiler'
    #------------------------

    #BUSCO LOS AVISOS
    params = {'condicion': condicion, 'localidad' : localidad, 'tipo' : tipo, 'visible' : 1 }
    params = {k: v for k, v in params.items() if v is not None and v != ''}

    try:
        propiedades = Propiedad.objects.filter(**params).order_by('-id')
    except:
        raise Http404

    context = {
        'propiedades' : propiedades,
        'tipos' : Tipo.objects.order_by('-id'),
        'localidades' : Localidad.objects.order_by('-id'),
        'titulo' : titulo,
        'navbar_active_propiedades': 'active',
    }
    return render_to_response('lista.html',context, context_instance=RequestContext(request))


def propiedad_detalle(request, tit_slug=''):
    propiedad = get_object_or_404(Propiedad, slug=tit_slug)

    propiedad_tipo = propiedad.tipo.id
    propiedad_condicion = propiedad.condicion
    propiedad_localidad = propiedad.localidad.id

    context = {
        'propiedad' : propiedad,
        'propiedades_relacionadas' : Propiedad.objects.filter(tipo=propiedad_tipo,localidad=propiedad_localidad,
                                                condicion=propiedad_condicion,visible=True).order_by('-id')[:30],
        'tipos' : Tipo.objects.order_by('-id'),
        'localidades' : Localidad.objects.order_by('-id'),
        'navbar_active_propiedades': 'active',
    }
    return render_to_response('propiedad.html',context, context_instance=RequestContext(request))

def servicios(request):
    context = {
        'navbar_active_servicios': 'active',
    }
    return render_to_response('servicios.html',context, context_instance=RequestContext(request))

def contacto(request):
    if request.method == 'POST':
        from django.conf import settings
        mail = {
            'subject' : request.POST['subject'],
            'name': request.POST['name'],
            'message': request.POST['message'],
            'from_email' : settings.DEFAULT_FROM_EMAIL,
            'reply_to' : request.POST['email'],
            'to': settings.DEFAULT_FROM_EMAIL,
        }
        if enviar_mail(mail=mail):
            messages.success(request, 'Gracias por contactarte, a la brevedad responderemos tu consulta.')

    propiedad = ''
    if request.method == 'GET':
        try:
            propiedad = Propiedad.objects.get(id=request.GET['id'])
        except:
            pass

    context = {
        'propiedad' : propiedad,
        'navbar_active_contacto': 'active',
    }
    return render_to_response('contacto.html',context, context_instance=RequestContext(request))