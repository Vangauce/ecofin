from django.shortcuts import render, redirect, get_object_or_404
from .models import Detalle_orden_venta,Ventas
from clientes.models import Clientes
from productos.models import Producto
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


# Create your views here.

def orden_venta_main(request):
    total_ordenes = Ventas.total_ordenes()
    return render(request, 'ventas/orden_venta_main.html', {'total_ordenes': total_ordenes})

from django.db.models import F
from django.db.models.functions import Cast
from django.db.models import IntegerField

def crear_orden_venta(request, id=None):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = Clientes.objects.get(pk=cliente_id)

        orden_venta = Ventas(clientes=cliente)
        orden_venta.save()

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        descuentos = request.POST.getlist('descuento')

        for i in range(len(productos)):
            producto_id = productos[i]
            cantidad = int(cantidades[i])
            precio = int(precios[i])
            descuento = int(descuentos[i])
            total_venta = cantidad * precio * (1 - descuento / 100)
            producto = Producto.objects.get(pk=producto_id)

            detalle = Detalle_orden_venta(
                venta=orden_venta,
                producto=producto,
                cantidad=cantidad,
                precio=precio,
                descuento=descuento,
                total_venta=total_venta
            )
            detalle.save()

            Producto.objects.filter(pk=producto_id).update(cantidad=Cast(F('cantidad'), IntegerField()) - cantidad)

        return redirect('detalle_orden_venta', orden_venta_id=orden_venta.id)
    else:
        clientes = Clientes.objects.all()
        productos = Producto.objects.all()
        return render(request, 'ventas/crear_orden_venta.html', {'clientes': clientes, 'productos': productos})



def eliminar_detalle_venta(request, id):
    detalle = Detalle_orden_venta.objects.get(pk=id)
    detalle.delete()
    return redirect('orden_venta_edit', id=detalle.venta.id)

def borrar_orden_venta(request, orden_venta_id):
    orden_venta = Ventas.objects.get(pk=orden_venta_id)
    orden_venta.delete()
    return redirect('listar_orden_venta')
from datetime import date

def detalle_orden_venta(request, orden_venta_id):
    orden_venta = Ventas.objects.get(pk=orden_venta_id)
    detalles = Detalle_orden_venta.objects.filter(venta=orden_venta)
    orden_venta.fecha = date.today()
    return render(request, 'ventas/detalle_orden_venta.html', {'orden_venta': orden_venta, 'detalles': detalles})

from django.db.models import Q

def listar_orden_venta(request):
    q = request.GET.get('q')
    fecha = request.GET.get('fecha')
    
    ordenes_venta = Ventas.objects.all()
    
    if q:
        ordenes_venta = ordenes_venta.filter(clientes__nombre__icontains=q)
    
    if fecha:
        ordenes_venta = ordenes_venta.filter(fecha=fecha)
    
    context = {
        'ordenes_venta': ordenes_venta,
    }
    
    return render(request, 'ventas/listar_orden_venta.html', context)



def editar_orden_venta(request, orden_venta_id):
    orden_venta = get_object_or_404(Ventas, id=orden_venta_id)

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Clientes, id=cliente_id)
        orden_venta.cliente = cliente
        orden_venta.save()

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        descuentos = request.POST.getlist('descuento')

        # Restablecer la cantidad de productos al valor original
        detalles_orden_venta = orden_venta.detalle_orden_venta_set.all()

        for detalle in detalles_orden_venta:
            producto = detalle.producto
            producto.cantidad += detalle.cantidad
            producto.save()

        # Eliminar los detalles de la orden de venta existentes
        detalles_orden_venta.delete()

        for i in range(len(productos)):
            producto = get_object_or_404(Producto, id=productos[i])
            cantidad = int(cantidades[i])
            precio = int(precios[i])
            descuento = int(descuentos[i])
            total_venta = cantidad * precio * (1 - descuento / 100)

            Detalle_orden_venta.objects.create(
                venta=orden_venta,
                producto=producto,
                cantidad=cantidad,
                precio=precio,
                descuento=descuento,
                total_venta=total_venta
            )

            # Restar la cantidad de la venta a la cantidad del producto
            producto.cantidad -= cantidad
            producto.save()

        return redirect('listar_orden_venta')

    clientes = Clientes.objects.all()
    productos = Producto.objects.all()
    context = {
        'orden_venta': orden_venta,
        'clientes': clientes,
        'productos': productos
    }
    return render(request, 'ventas/editar_orden_venta.html', context)

    
def generar_pdfventa(request):
    detalles_orden = Detalle_orden_venta.objects.select_related('venta').order_by('venta__id')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_venta.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Reporte de Ventas")

    font_size = 12
    y = 700
    x = 50

    total_ventas = 0

    venta_actual = None

    for detalle in detalles_orden:
        if venta_actual is None or venta_actual.id != detalle.venta.id:
            venta_actual = detalle.venta

            if y < 100:  # Si queda poco espacio en la página actual, crear una nueva página
                pdf.showPage()
                y = 700

            pdf.setFont('Helvetica-Bold', font_size)
            pdf.drawString(x, y, "ID de Venta: {}".format(venta_actual.id))
            pdf.setFont('Helvetica', font_size)
            y -= font_size + 10

            pdf.drawString(x, y, "Producto")
            pdf.drawString(x + 100, y, "Cantidad")
            pdf.drawString(x + 200, y, "Precio")
            pdf.drawString(x + 300, y, "Subtotal")
            pdf.drawString(x + 400, y, "Descuento")
            pdf.drawString(x + 500, y, "Total")
            y -= font_size + 10

        producto = detalle.producto.nombre
        cantidad = detalle.cantidad
        precio = detalle.precio
        sub_total = detalle.sub_total_detalle
        descuento = detalle.descuento_detalle
        total = detalle.total_detalle

        pdf.drawString(x, y, str(producto))
        pdf.drawString(x + 100, y, str(cantidad))
        pdf.drawString(x + 200, y, str(precio))
        pdf.drawString(x + 300, y, str(sub_total))
        pdf.drawString(x + 400, y, str(descuento))
        pdf.drawString(x + 500, y, str(total))
        y -= font_size + 2

    pdf.setFont('Helvetica', 10)

    pdf.showPage()
    pdf.save()

    request.session['redirigir_despues_de_descargar'] = True

    return response