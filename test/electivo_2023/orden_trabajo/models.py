from django.db import models
from ventas.models import Ventas


class OrdenTrabajo(models.Model):
    ventas = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    @classmethod
    def total_ordenes_trabajo(cls):
        return cls.objects.count()

    def obtener_estado_ventas(self):
        estado = self.ventas.estado
        return estado


