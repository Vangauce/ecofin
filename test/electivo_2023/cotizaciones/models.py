from django.db import models
from clientes.models import Clientes
from productos.models import Producto
import locale
class Cotizacion(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    fecha = models.DateField(auto_now_add=True)
    @classmethod
    def total_cotizaciones(cls):
        return cls.objects.count()

    def total(self):
        total = 0
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
        for item in self.detallecotizacion_set.all():
            total += item.subtotal()
        return locale.format_string('%d',total, grouping=True)

class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    descuento = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    total_coti = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    fecha = models.DateField

    def subtotal(self):
        return (self.cantidad * self.precio) * (1-self.descuento/100)
    
    def formatted_precio(self):
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') 
        return locale.format_string('%d', self.precio, grouping=True)
    
    def formatted_total_coti(self):
        locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8') 
        return locale.format_string('%d', self.total_coti, grouping=True)


    

