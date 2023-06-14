from django.db import models
from categorias.models import Categorias


class Producto(models.Model):  
    nombre = models.CharField(max_length=100)  
    cantidad = models.IntegerField() 
    material= models.CharField(max_length=15)  
    precio = models.CharField(max_length=20)
    categoria= models.ForeignKey(Categorias,on_delete=models.CASCADE)  
    can_sol=models.IntegerField(default=0)
    @classmethod
    def total_productos(cls):
        return cls.objects.count()
