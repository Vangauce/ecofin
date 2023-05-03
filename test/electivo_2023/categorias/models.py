from django.db import models



#class Categoria(models.Model):  #Position
    #title = models.CharField(max_length=50)

    #def __str__(self):
        #return self.title

<<<<<<< HEAD
class Categorias(models.Model):  #Employee
    nombre = models.CharField(max_length=100)  #fullname
    cantidad = models.IntegerField(default=0) #emp_code
    material= models.CharField(max_length=15)  #mobile
    #categoria= models.ForeignKey(Categoria,on_delete=models.CASCADE)  #position
=======
class Categorias(models.Model):  
    nombre = models.CharField(max_length=100)  
>>>>>>> 5f865d35fb26ace4a13a20975ad6cba52b3b7bda
    def __str__(self):
        return self.nombre
    @classmethod
    def total_categorias(cls):
        return cls.objects.count()  
