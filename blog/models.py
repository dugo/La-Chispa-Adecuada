# encoding=utf-8
from django.db import models
#from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Entry(models.Model):
    title = models.CharField(max_length=255)
    brief = models.CharField(max_length=255,blank=True,default='')
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True)
    public = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="images",blank=True,default='')
    author = models.ForeignKey(User)
    
    def save(self):
        
        """ Slug único si no lo tiene asignado """
        if not self.slug:
            original = self.slug = slugify(self.title)
            i=1
            while True:
                try:
                    entry = Entry.objects.all().get(slug=self.slug)
                except Entry.DoesNotExist:
                    break
                self.slug = original + "-%i" % i
                i+=1

            #self.image.name = 'images/'+self.slug+".jpg"
        
        super(Entry,self).save()
    
    def esta_publicado(self):
        if self.published:
            return u'Borrador'
        else:
            return u'Publicado'
    
    def __unicode__(self):
        return u"Autor: %s\nTitulo: %s" % (self.author.username,self.title)

class Comment(models.Model):
    entry = models.ForeignKey(Entry)
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    content = models.TextField(blank=True)
    
    def __unicode__(self):
        return u"Autor: %s Contenido: %s" % (self.author,self.content)
