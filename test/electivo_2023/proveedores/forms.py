from django import forms
from .models import Proveedores  
from django.forms import ModelForm




class ProveedoresForm(forms.ModelForm):  

    class Meta:
        model = Proveedores  
        fields = ('nombre', 'apellido', 'correo', 'direccion', 'telefono')
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'correo': 'Correo electrónico',
            'direccion': 'Dirección',
            'telefono': 'Teléfono'
        }
