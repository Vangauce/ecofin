from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Proveedores, Detalle_orden, Compras
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from productos.models import Producto

def orden_compra_main(request):
    return render(request, 'orden_compra/orden_compra_main.html')

def generar_pdf1(request):
    detalles_orden = Detalle_orden.objects.select_related('compra').order_by('compra__id')
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_compras.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Reporte de Compras")

    font_size = 12
    y = 700
    x = 50

    total_compras = 0

    compra_actual = None

    for detalle in detalles_orden:
        if compra_actual is None or compra_actual.id != detalle.compra.id:
            compra_actual = detalle.compra

            if y < 100:  # Si queda poco espacio en la página actual, crear una nueva página
                pdf.showPage()
                y = 700

            pdf.setFont('Helvetica-Bold', font_size)
            pdf.drawString(x, y, "ID de Compra: {}".format(compra_actual.id))
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

def crear_orden(request, id=None):
    proveedores = Proveedores.objects.all()
    productos = Producto.objects.all()

    template_name = 'orden_compra/crear_orden.html'
    detalle_orden = {}

    if request.method == "GET":
        compra = Compras.objects.filter(pk=id).first()

        if not compra:
            encabezado = {
                'id': 0,
                'proveedor': 0,
                'subTotal': 0,
                'descuento': 0,
                'total': 0
            }

            detalle_orden = None
        else:
            encabezado = {
                'id': compra.id,
                'proveedor': compra.proveedores,
                'subTotal': compra.sub_total,
                'descuento': compra.descuento,
                'total': compra.total
            }

            detalle_orden = Detalle_orden.objects.filter(compra=compra)

        context = {
            "compra": encabezado,
            "detallecompra": detalle_orden,
            "proveedores": proveedores,
            "productos": productos,
        }

        return render(request, template_name, context)

    if request.method == "POST":
        idProveedor = request.POST.get("proveedor")
        proveedor = Proveedores.objects.get(pk=idProveedor)

        if not id:
            compra = Compras(proveedores=proveedor)

            if compra:
                compra.save()

                id = compra.id
        else:
            compra = Compras.objects.filter(pk=id).first()

            if compra:
                compra.proveedores = proveedor

                compra.save()

        id_producto= request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        producto = Producto.objects.get(id=id_producto)
        desc = request.POST.get("descuento")

        sub_total_detalle = float(cantidad) * float(precio)
        descuento_detalle = float(desc)
        total_detalle = sub_total_detalle - descuento_detalle

        detalle_orden = Detalle_orden(compra=compra, producto=producto, cantidad=cantidad, precio=precio, sub_total_detalle=sub_total_detalle, descuento_detalle=descuento_detalle, total_detalle=total_detalle)

        if detalle_orden:
            detalle_orden.save()

        compra = Compras.objects.filter(pk=id).first()
        encabezado = {
            'id': compra.id,
            'proveedor': compra.proveedores,
            'subTotal': compra.sub_total,
            'descuento': compra.descuento,
            'total': compra.total
        }

        detalle_orden = Detalle_orden.objects.filter(compra=compra)

        context = {
            "compra": encabezado,
            "detallecompra": detalle_orden,
            "proveedores": proveedores,
            "productos": productos,
        }

        return redirect('orden_edit', id=compra.id)

    return render(request, template_name, {'proveedores': proveedores, 'productos': productos})


def ver_orden_compra(request, id):
    compra = Compras.objects.get(pk=id)
    detalles = Detalle_orden.objects.filter(compra=compra)
    context = {'compra': compra, 'detalles': detalles}
    return render(request, 'orden_compra/ver_orden_compra.html', context) 



def eliminar_detalle(request, id):
    detalle = Detalle_orden.objects.get(pk=id)
    detalle.delete()
    return redirect('orden_edit', id=detalle.compra.id)


def eliminar_orden_compra(request,id):
    compra = Compras.objects.get(pk=id)
    compra.delete()
    return redirect("/orden_compra/crear_orden/")

def listar_orden_compra(request):
    compras = Compras.objects.all()
    detalles = Detalle_orden.objects.all()
    context = {
        'compras': compras,
        'detalles': detalles,
    }
    return render(request, 'orden_compra/listar_orden_compra.html', context)
