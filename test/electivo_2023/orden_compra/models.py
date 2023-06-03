from django.db import models
from proveedores.models import Proveedores
from insumos.models import Insumos

class OrdenCompra(models.Model):
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    insumos = models.ManyToManyField(Insumos)
    fecha = models.DateField(auto_now_add=True)

    @classmethod
    def total_ordenes_compra(cls):
        return cls.objects.count()

    def total(self):
        total = 0
        for item in self.detalleordencompra_set.all():
            total += item.subtotal()
        return total

class DetalleOrdenCompra(models.Model):
    orden_compra = models.ForeignKey(OrdenCompra, on_delete=models.CASCADE)
    insumo = models.ForeignKey(Insumos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_compra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def subtotal(self):
        return (self.cantidad * self.precio) - self.descuento

