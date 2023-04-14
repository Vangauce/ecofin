from django.db import models

# Create your models here.

class Categoria(models.Model):  #Position
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Producto(models.Model):  #Employee
    nombre = models.CharField(max_length=100)  #fullname
    cantidad = models.CharField(max_length=3)  #emp_code
    material= models.CharField(max_length=15)  #mobile
    categoria= models.ForeignKey(Categoria,on_delete=models.CASCADE)  #position