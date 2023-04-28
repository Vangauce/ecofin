from django.db import models



#class Categoria(models.Model):  #Position
    #title = models.CharField(max_length=50)

    #def __str__(self):
        #return self.title

class Categorias(models.Model):  
    nombre = models.CharField(max_length=100)  
    def __str__(self):
        return self.nombre
    @classmethod
    def total_categorias(cls):
        return cls.objects.count()  
