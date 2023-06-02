from django.db import models
from ventas.models import Ventas


class OrdenTrabajo(models.Model):
    ventas = models.ForeignKey(Ventas, on_delete=models.CASCADE)


    def obtener_estado_ventas(self):
        estado = self.ventas.estado
        return estado


