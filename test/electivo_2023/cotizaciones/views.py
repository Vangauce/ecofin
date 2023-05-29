from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Cotizacion, DetalleCotizacion
from clientes.models import Clientes
from productos.models import Producto
from django.http import HttpResponse

from openpyxl import Workbook
from django.http import HttpResponse

def crear_cotizacion(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = Clientes.objects.get(pk=cliente_id)

        cotizacion = Cotizacion(cliente=cliente)
        cotizacion.save()

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')

        for i in range(len(productos)):
            producto_id = productos[i]
            cantidad = int(cantidades[i])
            precio = int(precios[i])

            producto = Producto.objects.get(pk=producto_id)

            detalle = DetalleCotizacion(cotizacion=cotizacion, producto=producto, cantidad=cantidad, precio=precio)
            detalle.save()

        return redirect('detalle_cotizacion', cotizacion_id=cotizacion.id)
    else:
        clientes = Clientes.objects.all()
        productos = Producto.objects.all()
        return render(request, 'crear_cotizacion.html', {'clientes': clientes, 'productos': productos})

def detalle_cotizacion(request, cotizacion_id):
    cotizacion = Cotizacion.objects.get(pk=cotizacion_id)
    detalles = DetalleCotizacion.objects.filter(cotizacion=cotizacion)
    return render(request, 'detalle_cotizacion.html', {'cotizacion': cotizacion, 'detalles': detalles})

def listado_cotizacion(request):
    cotizaciones = Cotizacion.objects.all()
    cotizaciones_dict = {}
    for cotizacion in cotizaciones:
        cotizacion_id = cotizacion.id
        if cotizacion_id in cotizaciones_dict:
            cotizaciones_dict[cotizacion_id]['cotizaciones'].append(cotizacion)
        else:
            cotizaciones_dict[cotizacion_id] = {'cotizaciones': [cotizacion]}
    borrar_url = reverse('borrar_cotizacion', kwargs={'cotizacion_id': 0})  # URL de borrado de cotización
    return render(request, 'listado_cotizaciones.html', {'cotizaciones_dict': cotizaciones_dict, 'borrar_url': borrar_url})

def borrar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    cotizacion.delete()
    return redirect('listado_cotizacion')

def obtener_datos_listado_cotizaciones():
    cotizaciones_dict = {}

    # Obtener todas las cotizaciones de la base de datos
    cotizaciones = Cotizacion.objects.all()

    # Organizar las cotizaciones por cotizacion_id y cliente
    for cotizacion in cotizaciones:
        cotizacion_id = cotizacion.id
        cliente = cotizacion.cliente

        if cotizacion_id not in cotizaciones_dict:
            cotizaciones_dict[cotizacion_id] = {'cliente': cliente, 'cotizaciones': []}

        cotizaciones_dict[cotizacion_id]['cotizaciones'].append(cotizacion)

    return cotizaciones_dict




def editar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    
    if request.method == 'POST':
        # Procesar los productos modificados en la cotización
        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        
        # Eliminar todos los detalles de la cotización existentes
        cotizacion.detallecotizacion_set.all().delete()
        
        # Agregar los nuevos detalles a la cotización
        for i in range(len(productos)):
            producto = get_object_or_404(Producto, id=productos[i])
            cantidad = cantidades[i]
            precio = precios[i]
            
            DetalleCotizacion.objects.create(
                cotizacion=cotizacion,
                producto=producto,
                cantidad=cantidad,
                precio=precio
            )
        
        # Redirigir a la página de listado de cotizaciones
        return redirect('listado_cotizacion')
    
    # Si es una solicitud GET, renderizar la plantilla de edición de cotización
    productos_disponibles = Producto.objects.all()
    context = {
        'cotizacion': cotizacion,
        'productos_disponibles': productos_disponibles
    }
    return render(request, 'editar_cotizacion.html', context)



def generar_reporte(request):
    cotizaciones_dict = obtener_datos_listado_cotizaciones()

    # Crear el archivo de Excel
    workbook = Workbook()
    sheet = workbook.active

    # Escribir encabezados
    sheet['A1'] = 'ID de Cotización'  # Nueva columna agregada
    sheet['B1'] = 'Cliente'
    sheet['C1'] = 'Producto'
    sheet['D1'] = 'Cantidad'
    sheet['E1'] = 'Precio'

    # Escribir datos de cotizaciones
    row = 2  # Comenzar desde la fila 2
    for cotizacion_id, data in cotizaciones_dict.items():
        cotizaciones = data['cotizaciones']
        cliente = data['cliente']

        for cotizacion in cotizaciones:
            for detalle in cotizacion.detallecotizacion_set.all():
                sheet[f'A{row}'] = cotizacion.id  # Nueva columna agregada
                sheet[f'B{row}'] = cliente.nombre
                sheet[f'C{row}'] = detalle.producto.nombre
                sheet[f'D{row}'] = detalle.cantidad
                sheet[f'E{row}'] = detalle.precio
                row += 1

    # Guardar el archivo de Excel en la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_cotizaciones.xlsx'
    workbook.save(response)

    return response



