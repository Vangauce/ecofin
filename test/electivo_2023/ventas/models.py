from django.db import models
from productos.models import Producto
from clientes.models import Clientes

# Create your models here.
class Ventas(models.Model):
    clientes = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    sub_total = models.FloatField(default=0) 
    descuento = models.FloatField(default=0) 
    total = models.FloatField(default=0) 
    estado = models.CharField(max_length=50, default='Pendiente')

    @classmethod
    def total_ordenes(cls):
        return cls.objects.count()


class Detalle_orden_venta(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.FloatField(default=0)
    sub_total_detalle = models.FloatField(default=0)
    descuento_detalle = models.FloatField(default=0)
    total_detalle = models.FloatField(default=0)

    def __str__(self):
        return '{}'.format(self.producto)
