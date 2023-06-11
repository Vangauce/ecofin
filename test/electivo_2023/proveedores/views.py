from django.shortcuts import render, redirect
from .models import Proveedores
from .forms import ProveedoresForm
import xlwt
import pandas as pd
from django.http import HttpResponse
from registration.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from productos.models import Producto
from django.http import JsonResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from itertools import groupby

@login_required
def carga_masiva_proveedores(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    template_name = 'proveedores/carga_masiva_proveedores.html'
    return render(request, template_name, {'profiles': profiles})


@login_required
def import_file_proveedores(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Apellido', 'Correo', 'Dirección', 'Teléfono']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    wb.save(response)
    return response


@login_required
def carga_masiva_proveedores_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        try:
            data = pd.read_excel(request.FILES['customFile'])
        except KeyError:
            messages.add_message(request, messages.ERROR, 'Debe seleccionar un archivo')
            return redirect('carga_masiva_proveedores')

        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            nombre = str(item[1])
            apellido = str(item[2])
            correo = str(item[3])
            direccion = str(item[4])
            telefono = str(item[5])
            proveedor = Proveedores(nombre=nombre, apellido=apellido, correo=correo, direccion=direccion, telefono=telefono)
            proveedor.save()
            acc += 1
        messages.add_message(request, messages.SUCCESS, f'Carga masiva finalizada, se importaron {acc} registros')
        return redirect('carga_masiva_proveedores')

    return redirect('carga_masiva_proveedores')


def proveedores_main(request):
    total_proveedores = Proveedores.total_proveedores()
    return render(request, 'proveedores/proveedores_main.html', {'total_proveedores': total_proveedores})

def proveedores_lista(request):
    q = request.GET.get('q')
    if q:
        proveedores_lista = Proveedores.objects.filter(nombre__icontains=q)
    else:
        proveedores_lista = Proveedores.objects.all()
    context = {'proveedores_lista': proveedores_lista}
    return render(request, "proveedores/proveedores_lista.html", context)


def proveedores_form(request,id=0):
    if request.method == "GET":
        if id ==0:
            form = ProveedoresForm()
        else:
            proveedores = Proveedores.objects.get(pk=id)
            form = ProveedoresForm(instance=proveedores)
        return render(request,"proveedores/proveedores_form.html",{'form':form})
    else:
        if id ==0 :
            form = ProveedoresForm(request.POST)
        else:
            proveedores = Proveedores.objects.get(pk=id)
            form = ProveedoresForm(request.POST,instance=proveedores)
        if form.is_valid():
            form.save()
        return redirect('/proveedores/list')

def proveedores_eliminar(request,id):
    proveedores = Proveedores.objects.get(pk=id)
    proveedores.delete()
    return redirect('/proveedores/list')

def proveedores_read(request, id):
    proveedores = Proveedores.objects.get(pk=id)
    context = {'proveedores': proveedores}
    return render(request, "proveedores/proveedores_read.html", context)





from reportlab.lib.pagesizes import letter
from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone

def generar_pdf(request):
    time_zone = pytz_timezone(settings.TIME_ZONE)  # Obtiene el objeto de zona horaria
    proveedores_lista = Proveedores.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_proveedores.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(100, 750, "Reportes EcoFácil")
    
    fecha_actual = timezone.now().astimezone(time_zone).strftime("%d/%m/%Y %H:%M:%S")
    pdf.setFont('Helvetica', 10)
    pdf.drawString(380, 750, f"Fecha del reporte: {fecha_actual}")

    y = 700
    x = 50

    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(x, y, "Reporte de Proveedores")
    pdf.setFont('Helvetica', 12)
    y -= 22

    pdf.drawString(x, y, "Nombre")
    pdf.drawString(x + 90, y, "Apellido")
    pdf.drawString(x + 170, y, "Correo")
    pdf.drawString(x + 330, y, "Dirección")
    pdf.drawString(x + 430, y, "Teléfono")
    y -= 18

    for proveedor in proveedores_lista:
        pdf.drawString(x, y, proveedor.nombre)
        pdf.drawString(x + 90, y, proveedor.apellido)
        pdf.drawString(x + 170, y, proveedor.correo)
        pdf.drawString(x + 330, y, proveedor.direccion)
        pdf.drawString(x + 430, y, proveedor.telefono)
        y -= 14

    pdf.showPage()
    pdf.save()

    request.session['redirigir_despues_de_descargar'] = True

    return response



