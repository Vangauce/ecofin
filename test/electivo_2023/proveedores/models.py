from django.db import models


class Proveedores(models.Model):  
    nombre = models.CharField(max_length=100)   
    direccion= models.CharField(max_length=15)
