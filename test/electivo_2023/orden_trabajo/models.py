from django.db import models
from ventas.models import Ventas


class OrdenTrabajo(models.Model):
    estado = models.CharField(max_length=100)

    def __str__(self):
        return self.estado


    
    ventas = models.ForeignKey(Ventas, on_delete=models.CASCADE, null = True)

    @classmethod
    def total_ordenes_trabajo(cls):
        return cls.objects.count()

    def obtener_estado_ventas(self):
        estado = self.ventas.estado
        return estado


