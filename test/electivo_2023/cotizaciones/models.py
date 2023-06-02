from django.db import models
from clientes.models import Clientes
from productos.models import Producto

class Cotizacion(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    fecha = models.DateField(auto_now_add=True)
    @classmethod
    def total_cotizaciones(cls):
        return cls.objects.count()

    def total(self):
        total = 0
        for item in self.productos.through.objects.filter(cotizacion=self):
            total += item.cantidad * item.precio
        return total

class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    fecha = models.DateField



    

