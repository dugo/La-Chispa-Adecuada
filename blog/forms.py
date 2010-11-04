# coding=utf-8
from blog.models import *
from django import forms

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('title', 'content', 'brief','image','public')

    def clean_title(self):
        if len(self.cleaned_data['title']) < 5:
            raise forms.ValidationError(u"Titulo demasiado escueto")
        return self.cleaned_data['title']
"""
def clean(self):
    try:
        if len(self.cleaned_data['title'])<len(self.cleaned_data['content']):
            raise forms.ValidationErros(u'El contenido es mas importante que la forma')
        return self.cleaned_data
    except KeyError:
        # Esta excepcion controla que existan las claves title y content en cleaned_data
        raise forms.ValidationError(u'Fallan los prerequisitos')
"""
