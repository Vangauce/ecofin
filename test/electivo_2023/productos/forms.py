from django import forms
from .models import Producto  #Employee
from django.forms import ModelForm


class AddSkillsForm:
    all_skills = forms.CharField(
        label="Skills ",
        widget=forms.HiddenInput(),
        required=False
    )

class ProductosForm(forms.ModelForm):  #EmployeeForm

    class Meta:
        model = Producto  #model = Employee
        fields = ('nombre','material','cantidad','categoria')
        labels = {
            'nombre':'Nombre',
            'cantidad':'n. cantidad'
        }

    def __init__(self, *args, **kwargs):
        super(ProductosForm,self).__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = "Select"
        self.fields['cantidad'].required = False