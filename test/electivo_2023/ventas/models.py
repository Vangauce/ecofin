from django.db import models
from productos.models import Producto
from clientes.models import Clientes
import locale

# Create your models here.
class Ventas(models.Model):
    clientes = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=50, default='Pendiente')

    @classmethod
    def total_ordenes(cls):
        return cls.objects.count()
    
    def total(self):
        total = 0
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') 
        for item in self.detalle_orden_venta_set.all():
            total += item.subtotal()
        return locale.format_string('%d',total, grouping=True)

class Detalle_orden_venta(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    descuento = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    total_venta = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    def subtotal(self):
        return (self.cantidad * self.precio) * (1-self.descuento/100)
    
    def formatted_precio(self):
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') 
        return locale.format_string('%d', self.precio, grouping=True)
    def formatted_total_venta(self):
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') 
        return locale.format_string('%d', self.total_venta, grouping=True)
    