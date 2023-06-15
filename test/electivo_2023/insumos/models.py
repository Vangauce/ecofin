from django.db import models



class Insumos(models.Model):  
    nombre = models.CharField(max_length=100) 
    cantidad = models.IntegerField() 
    material= models.CharField(max_length=15)
    precio = models.CharField(max_length=20)  
    can_sol=models.IntegerField(default=0) 
    @classmethod
    def total_insumos(cls):
        return cls.objects.count()  
