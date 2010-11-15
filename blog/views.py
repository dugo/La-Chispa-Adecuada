# coding=utf-8
# Create your views here.
from blog.models import *
from django.conf import settings
from django.shortcuts import get_object_or_404,render_to_response
from django.template import RequestContext
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseForbidden
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import Site, RequestSite
from django.utils import simplejson
from django.core.files.base import ContentFile
import re,os

from settings import ROOT_URL


from blog.forms import EntryForm

def index(request,last=False,slug=None):
    if last:
        entries = Entry.objects.all().order_by('-created')[:10]
    else:
        entries = Entry.objects.all().order_by('-created')
    
    return render_to_response('index.html', {'entries':entries,'expanded':not last,'slug':slug}, context_instance=RequestContext(request))

def page(request,slug):
	""" Carga la plantilla de entradas expandidas """
	
	# Carga la página
	entry = get_object_or_404(Entry,slug=slug)
	
	# Si la página no es publica y no pertenece al usuario actual (en caso de estar autentificado)
	if not entry.public and not (request.user.is_authenticated() and request.user==entry.author):
		# No se permitirá la entrada
		return HttpResponseForbidden('Acceso restringido')
		
	
	return render_to_response('page.html',dict(entry=entry),context_instance=RequestContext(request))

def comments(request,slug):
	
	if request.method == 'POST':
		""" Cuando llego aqui ya he comprobado los campos con js, aunque podría añadir un form """
		entry = get_object_or_404(Entry,slug=slug)
		comment = Comment(entry=entry,author=request.POST['name'],email=request.POST['email'],content=request.POST['comment'])
		comment.save()
		return HttpResponse('ok')
	else:
		return HttpResponseRedirect(ROOT_URL+'%s' % (slug))

@login_required
def edit(request,slug=None):

	entry = None
	
	if slug:
		try:
			entry = Entry.objects.get(slug=slug)
		except Entry.DoesNotExist:
			pass

	c = RequestContext(request)
	c.update(csrf(request))


	if request.method == 'POST':
		form = EntryForm(request.POST,request.FILES)

		if form.is_valid():
			# If editting
			if entry:
				entry.content = form.cleaned_data['content']
				entry.brief = form.cleaned_data['brief']
				entry.public = form.cleaned_data['public']
				entry.title = form.cleaned_data['title']
				entry.created = form.cleaned_data['created']
				if request.FILES.__contains__('image') and request.FILES['image']:
					try:
						entry.image.delete()
					except: pass
					entry.image.save(entry.slug+os.path.splitext( request.FILES['image'].name )[1],ContentFile(request.FILES['image'].read()))
					#handle_uploaded_file(request.FILES['image'],str(entry.image.file))
			# If NOT editting
			else:
				entry = form.save(commit=False)
				entry.author = request.user
				if request.FILES.__contains__('image') and request.FILES['image']:
					entry.image.save(entry.slug+os.path.splitext( request.FILES['image'].name )[1],ContentFile(request.FILES['image'].read()))
			
			entry.save()

			return HttpResponseRedirect(ROOT_URL)
		else:
			return HttpResponse(str(form.errors))
		
	form = EntryForm(instance=entry)
		
	return render_to_response('edit.html', dict(slug=slug,form=form), context_instance=c)

@never_cache
def loginajax(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """Displays the login form and handles the login action."""
    
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponse(redirect_to)

    else:
        form = authentication_form(request)
    
    request.session.set_test_cookie()
    
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    
    return HttpResponse('false')

@login_required
def delete(request,slug):
	
	entry = get_object_or_404(Entry,slug=slug)
	
	if request.user.is_authenticated() and request.user == entry.author:
		entry.delete()
	else:
		return HttpResponseForbidden('No es el autor de la página o no está autentificado')
	
	return HttpResponseRedirect(ROOT_URL)

# Supongo que todos los comentarios seran publicos => Sin control de autenticacion
def ajaxcomments(request,slug):
	try:
		entry = get_object_or_404(Entry,slug=slug)
		comments = Comment.objects.filter(entry = entry).order_by('-created')
	except Comment.DoesNotExist:
		return HttpResponse('')

	return render_to_response('ajaxcomments.html',dict(comments=comments))

def sitemap(request):
	entries = Entry.objects.all().order_by('-created')[:]
	last = entries[0].created
	
	return render_to_response('sitemap.xml',dict(entries=entries,last=last,HTTP_HOST='http://lachispaadecuada.dug0.com'),mimetype='application/xml')
