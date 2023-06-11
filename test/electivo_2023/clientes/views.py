from django.shortcuts import render, redirect
from .models import Clientes
from .forms import ClientesForm
import pandas as pd
from django.contrib import messages
from registration.models import Profile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import xlwt
from reportlab.pdfgen import canvas

def clientes_main(request):
    total_clientes = Clientes.total_clientes()
    return render(request, 'clientes/clientes_main.html', {'total_clientes': total_clientes})

def clientes_lista(request):
    q = request.GET.get('q')
    if q:
        clientes_lista = Clientes.objects.filter(nombre__icontains=q)
    else:
        clientes_lista = Clientes.objects.all()
    context = {'clientes_lista': clientes_lista}
    return render(request, "clientes/clientes_lista.html", context)


def clientes_form(request,id=0):
    if request.method == "GET":
        if id ==0:
            form = ClientesForm()
        else:
            clientes = Clientes.objects.get(pk=id)
            form = ClientesForm(instance=clientes)
        return render(request,"clientes/clientes_form.html",{'form':form})
    else:
        if id ==0 :
            form = ClientesForm(request.POST)
        else:
            clientes = Clientes.objects.get(pk=id)
            form = ClientesForm(request.POST,instance=clientes)
        if form.is_valid():
            form.save()
        return redirect('/clientes/list')

def clientes_eliminar(request,id):
    clientes = Clientes.objects.get(pk=id)
    clientes.delete()
    return redirect('/clientes/list')

def clientes_read(request, id):
    clientes = Clientes.objects.get(pk=id)
    context = {'clientes': clientes}
    return render(request, "clientes/clientes_read.html", context)




@login_required
def carga_masiva_clientes(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    template_name = 'clientes/carga_masiva_clientes.html'
    return render(request, template_name, {'profiles': profiles})


@login_required
def import_file_clientes(request):
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
def carga_masiva_clientes_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        try:
            data = pd.read_excel(request.FILES['customFile'])
        except KeyError:
            messages.add_message(request, messages.ERROR, 'Debe seleccionar un archivo')
            return redirect('carga_masiva_clientes')

        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            nombre = str(item[1])
            apellido = str(item[2])
            correo = str(item[3])
            direccion = str(item[4])
            telefono = str(item[5])
            cliente = Clientes(nombre=nombre, apellido=apellido, correo=correo, direccion=direccion, telefono=telefono)
            cliente.save()
            acc += 1
        messages.add_message(request, messages.SUCCESS, f'Carga masiva finalizada, se importaron {acc} registros')
        return redirect('carga_masiva_clientes')

    return redirect('carga_masiva_clientes')



from reportlab.lib.pagesizes import letter
from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone

@login_required
def generar_reporte_pdf(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una área para la que no tiene permisos')
        return redirect('check_group_main')
    time_zone = pytz_timezone(settings.TIME_ZONE) 
    clientes_lista = Clientes.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_clientes.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(100, 750, "Reportes EcoFácil")
    fecha_actual = timezone.now().astimezone(time_zone).strftime("%d/%m/%Y %H:%M:%S")
    pdf.setFont('Helvetica', 10)
    pdf.drawString(380, 750, f"Fecha del reporte: {fecha_actual}")
    y = 700
    x = 50
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(x, y, "Reporte de Clientes")
    pdf.setFont('Helvetica', 12)
    y -= 22
    pdf.drawString(x,y, "Nombre:")
    pdf.drawString(x + 90, y, "Apellido:")
    pdf.drawString(x + 190, y, "Correo:")
    pdf.drawString(x + 350, y, "Dirección:")
    pdf.drawString(x + 450, y, "Teléfono:")
    y -= 18
    for cliente in clientes_lista:
        pdf.drawString(x, y, cliente.nombre)
        pdf.drawString(x + 90, y, cliente.apellido)
        pdf.drawString(x + 190, y, cliente.correo)
        pdf.drawString(x + 350, y, cliente.direccion)
        pdf.drawString(x + 450, y, cliente.telefono)
        y -= 14
    
    pdf.showPage()
    pdf.save()

    request.session['redirigir_despues_de_descargar'] = True
    
    return response
