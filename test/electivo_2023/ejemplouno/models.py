from django.db import models

# Create your models here.

class Habilidad(models.Model):
    nombre=models.CharField(max_length=100,null=True,blank=True,verbose_name='Nombre habilidad')
    nivel=models.IntegerField(null=True, blank=True, verbose_name='Nivel Poder')
    estado=models.CharField(max_length=100,null=True,blank=True,default='Activo',verbose_name='Estado')
    created=models.DateTimeField(auto_now_add=True,verbose_name='Fecha Creación')
    updated=models.DateTimeField(auto_now=True,verbose_name='Fecha Actualización')
    class Meta:
        verbose_name='Habilidad'
        verbose_name_plural='Habilidades'
        ordering=['nombre']
    def __str__(self):
        return self.nombre

class Heroe(models.Model):
    Habilidad=models.ForeignKey(Habilidad, on_delete=models.CASCADE)
    nombre_heroe=models.CharField(max_length=100,null=True,blank=True)
    nacionalidad_heroe=models.CharField(max_length=100,null=True,blank=True)
    state=models.CharField(max_length=100,null=True,blank=True,default='Activo')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name='Heroe'
        verbose_name_plural='Heroes'
        ordering=['nombre_heroe']
    def __str__(self):
        return self.nombre_heroe