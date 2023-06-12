from django.shortcuts import render, redirect
from .models import Detalle_orden_venta,Ventas
from clientes.models import Clientes
from productos.models import Producto
from productos.models import Producto
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


# Create your views here.

def orden_venta_main(request):
    total_ordenes = Ventas.total_ordenes()
    return render(request, 'ventas/orden_venta_main.html', {'total_ordenes': total_ordenes})

def crear_orden_venta(request, id=None):
    clientes = Clientes.objects.all()
    productos = Producto.objects.all()

    template_name = 'ventas/crear_orden_venta.html'
    detalle_orden_venta = {}

    if request.method == "GET":
        venta = Ventas.objects.filter(pk=id).first()

        if not venta:
            encabezado = {
                'id': 0,
                'cliente': 0,
                'subTotal': 0,
                'descuento': 0,
                'total': 0
            }

            detalle_orden_venta = None
        else:
            encabezado = {
                'id': venta.id,
                'cliente': venta.clientes,
                'subTotal': venta.sub_total,
                'descuento': venta.descuento,
                'total': venta.total
            }

            detalle_orden_venta = Detalle_orden_venta.objects.filter(venta=venta)

        context = {
            "venta": encabezado,
            "detalleventa": detalle_orden_venta,
            "clientes": clientes,
            "productos": productos,
        }

        return render(request, template_name, context)

    if request.method == "POST":
        idCliente = request.POST.get("cliente")
        cliente = Clientes.objects.get(pk=idCliente)

        if not id:
            venta = Ventas(clientes=cliente)

            if venta:
                venta.save()

                id = venta.id
        else:
            venta = Ventas.objects.filter(pk=id).first()

            if venta:
                venta.clientes = cliente

                venta.save()

        id_producto= request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        producto = Producto.objects.get(id=id_producto)


        aa=producto.cantidad
        aa=int(aa)
        cantidad=int(cantidad)
        newca=aa-cantidad

        if newca<0:
            template_name='ventas/error.html'
            info = {
            "error":'La cantidad ingresada supera lo almacenado en el inventario'
            }
            return render(request, template_name, info)

        producto.cantidad=newca
        producto.save()




        desc = request.POST.get("descuento")

        sub_total_detalle = float(cantidad) * float(precio)
        descuento_detalle = float(desc)
        total_detalle = sub_total_detalle - descuento_detalle

        detalle_orden_venta = Detalle_orden_venta(venta=venta, producto=producto, cantidad=cantidad, precio=precio, sub_total_detalle=sub_total_detalle, descuento_detalle=descuento_detalle, total_detalle=total_detalle)

        if detalle_orden_venta:
            detalle_orden_venta.save()

        venta = Ventas.objects.filter(pk=id).first()
        encabezado = {
            'id': venta.id,
            'cliente': venta.clientes,
            'subTotal': venta.sub_total,
            'descuento': venta.descuento,
            'total': venta.total
        }

        detalle_orden_venta = Detalle_orden_venta.objects.filter(venta=venta)

        context = {
            "venta": encabezado,
            "detalleventa": detalle_orden_venta,
            "clientes": clientes,
            "productos": productos,
        }

        return redirect('orden_venta_edit', id=venta.id)

    return render(request, template_name, {'clientes': clientes, 'productos': productos})


def ver_orden_venta(request, id):
    venta = Ventas.objects.get(pk=id)
    detalles = Detalle_orden_venta.objects.filter(venta=venta)
    context = {'venta': venta, 'detalles': detalles}
    return render(request, 'ventas/ver_orden_venta.html', context) 

def eliminar_detalle_venta(request, id):
    detalle = Detalle_orden_venta.objects.get(pk=id)
    detalle.delete()
    return redirect('orden_venta_edit', id=detalle.venta.id)

def eliminar_orden_venta(request,id):
    venta = Ventas.objects.get(pk=id)
    venta.delete()
    return redirect("/ventas/crear_orden_venta/")

def listar_orden_venta(request):
    ventas = Ventas.objects.all()
    detalles = Detalle_orden_venta.objects.all()
    context = {
        'ventas': ventas,
        'detalles': detalles,
    }
    return render(request, 'ventas/listar_orden_venta.html', context)


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