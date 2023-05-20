from django import forms
from .models import Insumos  
from django.forms import ModelForm


class InsumosForm(forms.ModelForm):  

    class Meta:
        model = Insumos  
        fields = ('nombre','material','cantidad',)
        labels = {
            'nombre':'Nombre',
            'cantidad':'n. cantidad'
        }

    #def __init__(self, *args, **kwargs):
        #super(InsumosForm,self).__init__(*args, **kwargs)
        #self.fields['cantidad'].required = False
