from django import forms
from .models import Categorias  
from django.forms import ModelForm


class CategoriasForm(forms.ModelForm):  

    class Meta:
        model = Categorias  
        fields = ('nombre',)
        labels = {
            'nombre':'Nombre'

        }

