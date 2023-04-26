from django.db import models
from categorias.models import Categorias


class Producto(models.Model):  #Employee
    nombre = models.CharField(max_length=100)  #fullname
    cantidad = models.CharField(max_length=3)  #emp_code
    material= models.CharField(max_length=15)  #mobile
    categoria= models.ForeignKey(Categorias,on_delete=models.CASCADE)  #position

