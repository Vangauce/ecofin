from django.db import models

# Create your models here.

class Insumos(models.Model):  #Employee
    nombre = models.CharField(max_length=100)  #fullname
    cantidad = models.CharField(max_length=3)  #emp_code
    material= models.CharField(max_length=15)  #mobile
