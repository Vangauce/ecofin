from django.shortcuts import render, get_object_or_404, redirect
from ventas.models import Ventas, Detalle_orden_venta

from django.urls import reverse
from .models import OrdenTrabajo
from .forms import OrdenTrabajoForm
from registration.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import xlwt
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from reportlab.lib.pagesizes import letter


def carga_masiva_ordentrabajo(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    template_name = 'orden_trabajo/carga_masiva_ordentrabajo.html'
    return render(request, template_name, {'profiles': profiles})

@login_required
def carga_masiva_ordentrabajo_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        try:
            data = pd.read_excel(request.FILES['customFile'])
            df = pd.DataFrame(data)
            acc = 0
            for item in df.itertuples():
                estado = str(item[1])
                orden = OrdenTrabajo(estado=estado)
                orden.save()
                acc += 1
            messages.add_message(request, messages.INFO, f'Carga masiva finalizada, se importaron {acc} registros')
            return redirect('carga_masiva_ordentrabajo')
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'Error en la carga masiva: {str(e)}')
            return redirect('carga_masiva_ordentrabajo')
    else:

        return render(request, 'orden_trabajo/carga_masiva_ordentrabajo.html')
    
@login_required
def import_file_ordentrabajo(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Estado']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for row in range(1):
        row_num += 1
        for col_num in range(1):
            if col_num == 0:
                ws.write(row_num, col_num, 'Estado', font_style)
    wb.save(response)
    return response


def orden_trabajo_main(request):
    total_ordenes_trabajo = OrdenTrabajo.total_ordenes_trabajo()
    return render(request, 'orden_trabajo/orden_trabajo_main.html', {'total_ordenes_trabajo': total_ordenes_trabajo})

def ordentrabajo_lista(request):
    q = request.GET.get('q')
    if q:
        ordentrabajo_lista = OrdenTrabajo.objects.filter(estado__icontains=q)
    else:
        ordentrabajo_lista = OrdenTrabajo.objects.all()
    context = {'ordentrabajo_lista': ordentrabajo_lista}
    return render(request, "orden_trabajo/ordentrabajo_lista.html", context)



def listar_ventas(request):
    ventas = Ventas.objects.all()
    detalles = Detalle_orden_venta.objects.filter(venta__in=ventas)
    return render(request, 'orden_trabajo/listar_ventas.html', {'ventas': ventas, 'detalles': detalles})

def ordentrabajo_form(request,id=0):
    if request.method == "GET":
        if id == 0:
            form = OrdenTrabajoForm()
        else:
            ordenes = OrdenTrabajo.objects.get(pk=id)
            form = OrdenTrabajoForm(instance=ordenes)
        return render(request, "orden_trabajo/ordentrabajo_form.html",{'form': form})
    else:
        if id== 0 :
            form = OrdenTrabajoForm(request.POST)
        else:
            ordenes = OrdenTrabajo.objects.get(pk=id)
            form = OrdenTrabajoForm(request.POST,instance=ordenes)
        if form.is_valid():
            form.save()
        return redirect('/orden_trabajo/list')

def ordentrabajo_eliminar(request,id):
    ventas = Ventas.objects.get(pk=id)
    ventas.delete()
    return redirect('/orden_trabajo/listar_ventas')

def ordentrabajo_eliminar1(request,id):
    ordenes = OrdenTrabajo.objects.get(pk=id)
    ordenes.delete()
    return redirect('/orden_trabajo/list')

def ordentrabajo_read(request, id):
    ordenes= OrdenTrabajo.objects.get(pk=id)
    context = {'ordenes': ordenes}
    return render(request, "orden_trabajo/ordentrabajo_read.html",context)

def ver_estado_venta(request, id):
    venta = Ventas.objects.get(pk=id)
    ventas = [venta]  # Convertir la instancia en una lista de un solo elemento
    context = {'ventas': ventas}
    return render(request, 'orden_trabajo/ver_estado_venta.html', context)

def cambiar_estado_venta(request, id):
    venta = get_object_or_404(Ventas, pk=id)
    ordenes = OrdenTrabajo.objects.all()
    #estados = ['Pendiente', 'En bodega', 'En embalaje', 'En envío', 'Rechazado']
    estados_ordenes = [orden.estado for orden in ordenes]

    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        venta.estado = nuevo_estado
        venta.save()
        return redirect('listar_ventas') 

    context = {'venta': venta, 'estados_ordenes': estados_ordenes}
    #context = {'venta': venta, 'estados': estados}
    return render(request, 'orden_trabajo/cambiar_estado_venta.html', context)

from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone

def generar_reporte_pdf(request):
    time_zone = pytz_timezone(settings.TIME_ZONE)  # Obtiene el objeto de zona horaria
    ordenes_lista = OrdenTrabajo.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_ordenes.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(100, 750, "Reportes EcoFácil")
    fecha_actual = timezone.now().astimezone(time_zone).strftime("%d/%m/%Y %H:%M:%S")
    pdf.setFont('Helvetica', 10)
    pdf.drawString(380, 750, f"Fecha del reporte: {fecha_actual}")
    y = 700
    x = 50
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(x, y, "Reporte de Orden de Trabajo")
    pdf.setFont('Helvetica', 12)
    y -= 22
    pdf.drawString(x, y, "Estado:")
    y -= 18

    for orden in ordenes_lista:
        pdf.drawString(x, y, orden.estado)
        y -= 14
    pdf.showPage()
    pdf.save()

    request.session['redirigir_despues_de_descargar'] = True
    
    return response
