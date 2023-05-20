from django.db import models
from productos.models import Producto

class Proveedores(models.Model):  
    nombre = models.CharField(max_length=100)   
    direccion= models.CharField(max_length=15)
    @classmethod
    def total_proveedores(cls):
        return cls.objects.count()

    def __str__(self):
        return '{}'.format(self.producto)
