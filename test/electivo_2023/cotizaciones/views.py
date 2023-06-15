from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Cotizacion, DetalleCotizacion
from clientes.models import Clientes
from productos.models import Producto
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.views import View
from django.template.loader import get_template

from openpyxl import Workbook
from django.http import HttpResponse

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

def cotizaciones_main(request):
    total_cotizaciones = Cotizacion.total_cotizaciones()
    return render(request, 'cotizaciones_main.html',{'total_cotizaciones': total_cotizaciones})

import io
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.text import slugify
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Cotizacion, DetalleCotizacion, Clientes
from .forms import CotizacionForm

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def enviar_correo_cliente(cotizacion, pdf):
    # Obtener la información del cliente
    cliente = cotizacion.cliente
    nombre_cliente = cliente.nombre
    correo_cliente = cliente.correo
    apellido_cliente = cliente.apellido
    # Asunto y contenido del correo
    asunto = 'Cotización Generada'
    mensaje_html = render_to_string('emails/correo_cotizacion.html', {'nombre_cliente': nombre_cliente, 'apellido_cliente': apellido_cliente})
    mensaje_texto = strip_tags(mensaje_html)

    # Configurar el correo
    correo = EmailMultiAlternatives(asunto, mensaje_texto, 'uautonomachatgpt@gmail.com', [correo_cliente])
    correo.attach_alternative(mensaje_html, 'text/html')

    # Adjuntar el PDF
    archivo_pdf = f'{nombre_cliente}-cotizacion.pdf'
    correo.attach(archivo_pdf, pdf.getvalue(), 'application/pdf')

    # Enviar el correo
    correo.send()

@login_required
def crear_cotizacion(request):
    clientes = Clientes.objects.all()
    productos = Producto.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        cliente = Clientes.objects.get(pk=cliente_id)

        cotizacion = Cotizacion(cliente=cliente)
        cotizacion.save()

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        descuentos = request.POST.getlist('descuento')

        for i in range(len(productos)):
            producto_id = productos[i]
            cantidad = int(cantidades[i])
            precio = int(precios[i])
            descuento = int(descuentos[i])
            total_coti = cantidad * precio * (1 - descuento / 100)
            producto = Producto.objects.get(pk=producto_id)

            detalle = DetalleCotizacion(cotizacion=cotizacion, producto=producto, cantidad=cantidad, precio=precio, descuento=descuento, total_coti=total_coti)
            detalle.save()

        # Generar el PDF
        response = generar_reporte_pdf(request, cotizacion.id)

        # Enviar el correo al cliente con el PDF adjunto
        enviar_correo_cliente(cotizacion, response)
        messages.success(request, 'La cotización se ha creado correctamente y se ha enviado al cliente.')
        
        return redirect('detalle_cotizacion', cotizacion_id=cotizacion.id)  
 

    else:
        return render(request, 'crear_cotizacion.html', {'clientes': clientes, 'productos': productos})




from datetime import date

def detalle_cotizacion(request, cotizacion_id):
    cotizacion = Cotizacion.objects.get(pk=cotizacion_id)
    detalles = DetalleCotizacion.objects.filter(cotizacion=cotizacion)
    
    # fecha modificacion
    cotizacion.fecha = date.today()
    
    return render(request, 'detalle_cotizacion.html', {'cotizacion': cotizacion, 'detalles': detalles})


def listado_cotizacion(request):
    q = request.GET.get('q')
    fecha = request.GET.get('fecha')
    
    cotizaciones = Cotizacion.objects.all()
    
    if q:
        cotizaciones = cotizaciones.filter(cliente__nombre__icontains=q)
    
    if fecha:
        cotizaciones = cotizaciones.filter(fecha=fecha)
    
    context = {
        'cotizaciones': cotizaciones,
    }
    
    return render(request, 'listado_cotizaciones.html', context)

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
        cliente_id = request.POST.get('cliente')
        cliente = get_object_or_404(Clientes, id=cliente_id)
        cotizacion.cliente = cliente
        cotizacion.save()

        productos = request.POST.getlist('producto')
        cantidades = request.POST.getlist('cantidad')
        precios = request.POST.getlist('precio')
        descuentos = request.POST.getlist('descuento')
        
        # Eliminar todos los detalles de la cotización existentes
        cotizacion.detallecotizacion_set.all().delete()
        
        # Agregar los nuevos detalles a la cotización
        for i in range(len(productos)):
            producto = get_object_or_404(Producto, id=productos[i])
            cantidad = int(cantidades[i])
            precio = int(precios[i])
            descuento = int(descuentos[i])
            total_coti = cantidad * precio * (1 - descuento / 100)
            DetalleCotizacion.objects.create(
                cotizacion=cotizacion,
                producto=producto,
                cantidad=cantidad,
                precio=precio,
                descuento=descuento,
                total_coti=total_coti
            )
        
        # Redirigir a la página de listado de cotizaciones
        return redirect('listado_cotizacion')
    
    clientes = Clientes.objects.all()
    productos_disponibles = Producto.objects.all()
    context = {
        'cotizacion': cotizacion,
        'clientes': clientes,
        'productos_disponibles': productos_disponibles
    }
    return render(request, 'editar_cotizacion.html', context)


def generar_reporte(request):
    cotizaciones_dict = obtener_datos_listado_cotizaciones()

    # Crear el archivo de Excel
    workbook = Workbook()
    sheet = workbook.active

    # Escribir encabezados
    sheet['J1'] = 'Fecha'
    sheet['A1'] = 'ID de Cotización'
    sheet['B1'] = 'Cliente'
    sheet['C1'] = 'Apellido'
    sheet['D1'] = 'Producto'
    sheet['E1'] = 'Cantidad'
    sheet['F1'] = 'Precio'
    sheet['G1'] = 'Descuento (%)'
    sheet['H1'] = 'Subtotal'
    sheet['I1'] = 'Total'

    # Aplicar formato de negrita a la fila 1
    for cell in sheet[1]:
        cell.font = cell.font.copy(bold=True)

    # Escribir datos de cotizaciones
    row = 2  # Comenzar desde la fila 2
    id_anterior = None
    for cotizacion_id, data in cotizaciones_dict.items():
        cotizaciones = data['cotizaciones']
        cliente = data['cliente']

        total = 0  # Variable para almacenar el total de la cotización

        for cotizacion in cotizaciones:
            if cotizacion.id != id_anterior:
                row += 1
                total = 0  # Reiniciar el total para el nuevo ID de cotización
            id_anterior = cotizacion.id

            for detalle in cotizacion.detallecotizacion_set.all():
                sheet[f'J{row}'] = cotizacion.fecha
                sheet[f'A{row}'] = cotizacion.id
                sheet[f'B{row}'] = cliente.nombre
                sheet[f'C{row}'] = cliente.apellido
                sheet[f'D{row}'] = detalle.producto.nombre
                sheet[f'E{row}'] = detalle.cantidad
                sheet[f'F{row}'] = detalle.precio
                sheet[f'G{row}'] = detalle.descuento

                subtotal = detalle.cantidad * detalle.precio * (100 - detalle.descuento) / 100
                sheet[f'H{row}'] = subtotal

                total += subtotal  # Acumular el subtotal en el total de la cotización

                row += 1

            sheet[f'I{row - 1}'] = total  # Escribir el total en la última fila de la cotización

    # Guardar el archivo de Excel en la respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_cotizaciones.xlsx'
    workbook.save(response)

    return response


from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib import colors
from django.http import HttpResponse
from django.utils.text import slugify

def generar_reporte_pdf(request, cotizacion_id):
    # Obtener la cotización específica
    cotizacion = Cotizacion.objects.get(id=cotizacion_id)

    # Crear el objeto PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{slugify(cotizacion.cliente.nombre)}-cotizacion.pdf"'

    # Crear el documento PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Lista de elementos del PDF
    elements = []

    # Estilos de la tabla
    styles = getSampleStyleSheet()
    estilo_cabecera = styles['Heading4']
    estilo_normal = styles['Normal']

    # Encabezado del PDF
    encabezado = Paragraph("Detalle Cotización", estilo_cabecera)
    elements.append(encabezado)

    # Información del cliente
    cliente_info = f"<b>Cliente:</b> {cotizacion.cliente.nombre}<br/>"
    cliente_info += f"<b>E-mail:</b> {cotizacion.cliente.correo}<br/>"
    cliente_info += f"<b>Dirección:</b> {cotizacion.cliente.direccion}<br/>"
    cliente_info += f"<b>Teléfono:</b> {cotizacion.cliente.telefono}<br/>"
    cliente_info += f"<b>Fecha:</b> {cotizacion.fecha}"
    cliente_info_paragraph = Paragraph(cliente_info, estilo_normal)
    elements.append(cliente_info_paragraph)

    # Tabla de detalles de la cotización
    detalles_table_data = []
    detalles_table_data.append(["Producto", "Cantidad", "Precio", "Descuento (%)", "Total"])

    for detalle in cotizacion.detallecotizacion_set.all():
        detalles_table_data.append([
            detalle.producto.nombre,
            str(detalle.cantidad),
            str(detalle.precio),
            str(detalle.descuento),
            str(detalle.subtotal())
        ])

    detalles_table = Table(detalles_table_data)
    detalles_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), estilo_cabecera.backColor),
        ("TEXTCOLOR", (0, 0), (-1, 0), estilo_cabecera.textColor),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), estilo_cabecera.fontName),
        ("FONTSIZE", (0, 0), (-1, 0), estilo_cabecera.fontSize),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(detalles_table)

    # Total de la cotización
    total = f"<b>Total Orden de Venta:</b> {cotizacion.total()}"
    total_paragraph = Paragraph(total, estilo_normal)
    elements.append(total_paragraph)

    # Construir el PDF
    pdf.build(elements)

    return response

from reportlab.lib.pagesizes import letter
from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone
from registration.models import Profile

@login_required
def generar_reporte_general_pdf(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    time_zone = pytz_timezone(settings.TIME_ZONE) 
    listado_cotizaciones = Cotizacion.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_Cotizacion.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(100, 750, "Reportes EcoFácil")
    fecha_actual = timezone.now().astimezone(time_zone).strftime("%d/%m/%Y %H:%M:%S")
    pdf.setFont('Helvetica', 10)
    pdf.drawString(380, 750, f"Fecha del reporte: {fecha_actual}")
    y = 700
    x = 50
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(x, y, "Reporte de Cotizaciones")
    pdf.setFont('Helvetica', 12)
    y -= 22
    pdf.drawString(x,y, "Orden:")
    pdf.drawString(x + 50, y, "Cliente:")
    pdf.drawString(x + 100, y, "Apellido:")
    pdf.drawString(x + 180, y, "Fecha:")
    pdf.drawString(x + 290, y, "Dirección:")
    pdf.drawString(x + 420, y, "Total:")
    y -= 18
    for cotizacion in listado_cotizaciones:
        pdf.drawString(x, y, str(cotizacion.id))
        pdf.drawString(x + 50, y, cotizacion.cliente.nombre)
        pdf.drawString(x + 100, y, cotizacion.cliente.apellido)
        pdf.drawString(x + 180, y, str(cotizacion.fecha))
        pdf.drawString(x + 290, y, cotizacion.cliente.direccion)
        pdf.drawString(x + 420, y, str(cotizacion.total))
        y -= 14
    
    pdf.showPage()
    pdf.save()

    request.session['redirigir_despues_de_descargar'] = True
    
    return response
