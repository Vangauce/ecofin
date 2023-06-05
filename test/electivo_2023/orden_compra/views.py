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
    ordenes_compra = OrdenCompra.objects.all()
    ordenes_compra_dict = {}
    for orden_compra in ordenes_compra:
        orden_compra_id = orden_compra.id
        if orden_compra_id in ordenes_compra_dict:
            ordenes_compra_dict[orden_compra_id]['ordenes_compra'].append(orden_compra)
        else:
            ordenes_compra_dict[orden_compra_id] = {'ordenes_compra': [orden_compra]}
    borrar_url = reverse('borrar_orden_compra', kwargs={'orden_compra_id': 0})  # URL de borrado de orden de compra
    return render(request, 'listado_orden_compra.html', {'ordenes_compra_dict': ordenes_compra_dict, 'borrar_url': borrar_url})

def borrar_orden_compra(request, orden_compra_id):
    orden_compra = get_object_or_404(OrdenCompra, id=orden_compra_id)
    orden_compra.delete()
    return redirect('listado_orden_compra')

def obtener_datos_listado_ordenes_compra():
    ordenes_compra_dict = {}

    # Obtener todas las órdenes de compra de la base de datos
    ordenes_compra = OrdenCompra.objects.all()

    # Organizar las órdenes de compra por orden_compra_id y proveedor
    for orden_compra in ordenes_compra:
        orden_compra_id = orden_compra.id
        proveedor = orden_compra.proveedor

        if orden_compra_id not in ordenes_compra_dict:
            ordenes_compra_dict[orden_compra_id] = {'proveedor': proveedor, 'ordenes_compra': []}

        ordenes_compra_dict[orden_compra_id]['ordenes_compra'].append(orden_compra)

    return ordenes_compra_dict


def editar_orden_compra(request, orden_compra_id):
    orden_compra = get_object_or_404(OrdenCompra, id=orden_compra_id)
    
    if request.method == 'POST':
        # Procesar los insumos modificados en la orden de compra
        insumos = request.POST.getlist('insumo')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        
        # Eliminar todos los detalles de la orden de compra existentes
        orden_compra.detalleordencompra_set.all().delete()
        
        # Agregar los nuevos detalles a la orden de compra
        for i in range(len(insumos)):
            insumo = get_object_or_404(Insumos, id=insumos[i])
            cantidad = cantidades[i]
            precio = precios[i]
            
            DetalleOrdenCompra.objects.create(
                orden_compra=orden_compra,
                insumo=insumo,
                cantidad=cantidad,
                precio=precio
            )
        
        # Redirigir a la página de listado de órdenes de compra
        return redirect('listado_ordenes_compra')
    
    # Si es una solicitud GET, renderizar la plantilla de edición de orden de compra
    insumos_disponibles = Insumos.objects.all()
    context = {
        'orden_compra': orden_compra,
        'insumos_disponibles': insumos_disponibles
    }
    return render(request, 'editar_orden_compra.html', context)


def generar_reporte(request):
    ordenes_compra_dict = obtener_datos_listado_ordenes_compra()

    # Crear el archivo de Excel
    workbook = Workbook()
    sheet = workbook.active

    # Escribir encabezados
    sheet['H1'] = 'Fecha'
    sheet['A1'] = 'ID de Orden de Compra'
    sheet['B1'] = 'Proveedor'
    sheet['C1'] = 'Insumo'
    sheet['D1'] = 'Cantidad'
    sheet['E1'] = 'Precio'
    sheet['F1'] = 'Subtotal'
    sheet['G1'] = 'Total'

    # Aplicar formato de negrita a la fila 1
    for cell in sheet[1]:
        cell.font = cell.font.copy(bold=True)

    # Escribir datos de órdenes de compra
    row = 2  # Comenzar desde la fila 2
    id_anterior = None
    for orden_compra_id, data in ordenes_compra_dict.items():
        ordenes_compra = data['ordenes_compra']
        proveedor = data['proveedor']

        total = 0  # Variable para almacenar el total de la orden de compra

        for orden_compra in ordenes_compra:
            if orden_compra.id != id_anterior:
                row += 1
                total = 0  # Reiniciar el total para el nuevo ID de orden de compra
            id_anterior = orden_compra.id

            for detalle in orden_compra.detalleordencompra_set.all():
                sheet[f'H{row}'] = orden_compra.fecha
                sheet[f'A{row}'] = orden_compra.id
                sheet[f'B{row}'] = proveedor.nombre
                sheet[f'C{row}'] = detalle.insumo.nombre
                sheet[f'D{row}'] = detalle.cantidad
                sheet[f'E{row}'] = detalle.precio

                subtotal = detalle.cantidad * detalle.precio
                sheet[f'F{row}'] = subtotal

                total += subtotal  # Acumular el subtotal en el total de la orden de compra

                row += 1

            sheet[f'G{row - 1}'] = total  # Escribir el total en la última fila de la orden de compra

    # Guardar el archivo de Excel en la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_ordenes_compra.xlsx'
    workbook.save(response)

    return response
