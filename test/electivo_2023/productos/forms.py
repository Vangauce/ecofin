from django import forms
from .models import Producto  
from django.forms import ModelForm




class ProductosForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('nombre', 'material', 'cantidad', 'categoria', 'precio')
        labels = {
            'nombre': 'Nombre',
            'cantidad': 'Cantidad',
            'precio': 'Precio'
        }

    def __init__(self, *args, **kwargs):
        super(ProductosForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = "Select"
        self.fields['cantidad'].required = False

