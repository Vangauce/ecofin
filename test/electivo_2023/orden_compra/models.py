from django.db import models
from proveedores.models import Proveedores
from insumos.models import Insumos
import locale

class OrdenCompra(models.Model):
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    insumos = models.ManyToManyField(Insumos)
    fecha = models.DateField(auto_now_add=True)

    @classmethod
    def total_ordenes_compra(cls):
        return cls.objects.count()

    def total(self):
        total = 0
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') 
        for item in self.detalleordencompra_set.all():
            total += item.subtotal()
        return locale.format_string('%d',total, grouping=True)
    


class DetalleOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    descuento = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    total_compra = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)

    def subtotal(self):
        return (self.cantidad * self.precio) * (1-self.descuento/100)
    
    def formatted_precio(self):
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') 
        return locale.format_string('%d', self.precio, grouping=True)
    def formatted_total_compra(self):
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') 
        return locale.format_string('%d', self.total_compra, grouping=True)

