from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import OrdenCompra, DetalleOrdenCompra
from proveedores.models import Proveedores
from insumos.models import Insumos
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.views import View
from django.template.loader import get_template
from django.db.models import F
from django.db.models.functions import Cast
from django.db.models import IntegerField
from openpyxl import Workbook
from django.http import HttpResponse

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def ordenes_compra_main(request):
    total_ordenes_compra = OrdenCompra.total_ordenes_compra()
    return render(request, 'orden_compra_main.html',{'total_ordenes_compra': total_ordenes_compra})

def crear_orden_compra(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        proveedor = Proveedores.objects.get(pk=proveedor_id)

        orden_compra = OrdenCompra(proveedor=proveedor)
        orden_compra.save()

        insumos = request.POST.getlist('insumo')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        descuentos = request.POST.getlist('descuento')  # Agregar esta línea para obtener los descuentos

        for i in range(len(insumos)):
            insumo_id = insumos[i]
            cantidad = int(cantidades[i])
            precio = int(precios[i])
            descuento = int(descuentos[i])  # Obtener el descuento correspondiente
            total_compra = cantidad*precio*(1-descuento/100)

            insumo = Insumos.objects.get(pk=insumo_id)

            detalle = DetalleOrdenCompra(orden_compra=orden_compra, insumo=insumo, cantidad=cantidad, precio=precio, descuento=descuento,total_compra=total_compra)  # Agregar el descuento al crear el objeto DetalleOrdenCompra
            detalle.save()
            Insumos.objects.filter(pk=insumo_id).update(cantidad=Cast(F('cantidad'), IntegerField()) + cantidad)
        return redirect('detalle_orden_compra', orden_compra_id=orden_compra.id)
    else:
        proveedores = Proveedores.objects.all()
        insumos = Insumos.objects.all()
        return render(request, 'crear_orden_compra.html', {'proveedores': proveedores, 'insumos': insumos})

from datetime import date

def detalle_orden_compra(request, orden_compra_id):
    orden_compra = OrdenCompra.objects.get(pk=orden_compra_id)
    detalles = DetalleOrdenCompra.objects.filter(orden_compra=orden_compra)

    # fecha modificacion
    orden_compra.fecha = date.today()
    return render(request, 'detalle_orden_compra.html', {'orden_compra': orden_compra, 'detalles': detalles})


def listado_orden_compra(request):
    q = request.GET.get('q')
    ordenes_compra = OrdenCompra.objects.all()
    if q:
        ordenes_compra = ordenes_compra.filter(proveedor__nombre__icontains=q)
        
    return render(request, 'listado_orden_compra.html', {'ordenes_compra': ordenes_compra})


def borrar_orden_compra(request, orden_compra_id):
    orden_compra = OrdenCompra.objects.get(pk=orden_compra_id)
    orden_compra.delete()
    return redirect('listado_ordenes_compra')




def editar_orden_compra(request, orden_compra_id):
    orden_compra = get_object_or_404(OrdenCompra, id=orden_compra_id)

    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        proveedor = get_object_or_404(Proveedores, id=proveedor_id)
        orden_compra.proveedor = proveedor
        orden_compra.save()

        insumos = request.POST.getlist('insumo')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        descuentos = request.POST.getlist('descuento')

        # Restablecer la cantidad de insumos al valor original
        detalles_orden_compra = orden_compra.detalleordencompra_set.all()

        for detalle in detalles_orden_compra:
            insumo = detalle.insumo
            insumo.cantidad -= detalle.cantidad
            insumo.save()

        detalles_orden_compra.delete()

        for i in range(len(insumos)):
            insumo = get_object_or_404(Insumos, id=insumos[i])
            cantidad = int(cantidades[i])
            precio = int(precios[i])
            descuento = int(descuentos[i])
            total_compra = cantidad * precio * (1 - descuento / 100)

            DetalleOrdenCompra.objects.create(
                orden_compra=orden_compra,
                insumo=insumo,
                cantidad=cantidad,
                precio=precio,
                descuento=descuento,
                total_compra=total_compra
            )

            # Reducir la cantidad de insumos según la compra realizada
            insumo.cantidad += cantidad
            insumo.save()

        return redirect('listado_ordenes_compra')

    proveedores = Proveedores.objects.all()
    insumos = Insumos.objects.all()
    context = {
        'orden_compra': orden_compra,
        'proveedores': proveedores,
        'insumos': insumos
    }
    return render(request, 'editar_orden_compra.html', context)


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils import timezone
from pytz import timezone as pytz_timezone
import pytz

def generar_reporte_orden_compra(request):
    time_zone = pytz.timezone(settings.TIME_ZONE)
    ordenes_compra = OrdenCompra.objects.all().select_related('proveedor').prefetch_related('insumos')
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=reporte_ordenes_compra.pdf'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont('Helvetica-Bold', 12)
    p.drawString(100, 750, "Reportes EcoFácil")
    
    fecha_actual = timezone.now().astimezone(time_zone).strftime("%d/%m/%Y %H:%M:%S")
    p.setFont('Helvetica', 10)
    p.drawString(380, 750, f"Fecha del reporte: {fecha_actual}")
    
    x = 50
    y = 700
    
    p.setFont('Helvetica-Bold', 12)
    p.drawString(x, y, "Reporte de órdenes de compra")
    
    p.setFont('Helvetica', 12)
    y -= 22
    
    p.drawString(x, y, 'ID')
    p.drawString(x + 70, y, 'Proveedor')
    p.drawString(x + 140, y, 'Insumo')
    p.drawString(x + 230, y, 'Cantidad')
    p.drawString(x + 300, y, 'Precio')
    p.drawString(x + 370, y, 'Subtotal')
    p.drawString(x + 440, y, 'Total')
    
    y -= 18
    
    for orden_compra in ordenes_compra:
        proveedor = orden_compra.proveedor.nombre
        total = orden_compra.total()
    
        p.setFont("Helvetica", 12)
        p.drawString(x, y, str(orden_compra.id))
        p.drawString(x + 70, y, proveedor)
    
        for detalle in orden_compra.detalleordencompra_set.all():
            insumo = detalle.insumo.nombre
            cantidad = str(detalle.cantidad)
            precio = detalle.formatted_precio()
            subtotal = detalle.subtotal()
    
            p.drawString(x + 140, y, insumo)
            p.drawString(x + 230, y, cantidad)
            p.drawString(x + 300, y, precio)
            p.drawString(x + 370, y, str(subtotal))
    
        #p.drawString(x + 650, y, total)
        y -= 14
    
        if y <= 100:
            p.showPage()
            y = 720
    
    p.save()
    
    return response
