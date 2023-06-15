from django import forms
from .models import OrdenTrabajo 
from django.forms import ModelForm


class OrdenTrabajoForm(forms.ModelForm):  

    class Meta:
        model = OrdenTrabajo  
        fields = ('estado',)
        labels = {
            'estado':'Estado',

        }