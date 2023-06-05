from django.db import models


class Proveedores(models.Model):  
    nombre = models.CharField(max_length=100)   
    apellido = models.CharField(max_length=100) 
    correo = models.CharField(max_length=100) 
    direccion = models.CharField(max_length=20)
    telefono = models.CharField(max_length=10) 
    @classmethod
    def total_proveedores(cls):
        return cls.objects.count()


