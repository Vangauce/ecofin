from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductosForm
import xlwt
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto
from registration.models import Profile
from categorias.models import Categorias
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from reportlab.lib.pagesizes import letter



def carga_masiva_productos(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    categorias = Categorias.objects.all() #obtener todas las categorias
    template_name = 'productos/carga_masiva_productos.html'
    return render(request, template_name, {'profiles': profiles, 'categorias': categorias})

@login_required
def carga_masiva_productos_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        try:
            data = pd.read_excel(request.FILES['customFile'])
        except KeyError:
            messages.add_message(request, messages.ERROR, 'Debe seleccionar un archivo')
            return redirect('carga_masiva_productos')
            
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            nombre = str(item[1])
            cantidad = str(item[2])
            material = str(item[3])
            try:
                categoria = Categorias.objects.get(nombre=item[4]) 
            except Categorias.DoesNotExist:
                messages.add_message(request, messages.ERROR, f'El producto "{item[4]}" no existe')
                return redirect('carga_masiva_productos')
                
            producto = Producto(nombre=nombre, cantidad=cantidad, material=material, categoria=categoria)
            producto.save()
            acc += 1
        messages.add_message(request, messages.SUCCESS, f'Carga masiva finalizada, se importaron {acc} registros')
        return redirect('carga_masiva_productos')

@login_required
def import_file_productos(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Cantidad', 'Material', 'Categoría']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(4):
            if col_num == 0:
                ws.write(row_num, col_num, 'Nombre del producto', font_style)
            elif col_num == 1:
                ws.write(row_num, col_num, 'Cantidad disponible', font_style)
            elif col_num == 2:
                ws.write(row_num, col_num, 'Material del producto', font_style)
            elif col_num == 3:
                ws.write(row_num, col_num, 'Categoría del producto', font_style)
    wb.save(response)
    return response


def productos_main(request):
    total_productos = Producto.total_productos()
    return render(request, 'productos/productos_main.html', {'total_productos': total_productos})

def productos_lista(request):
    q = request.GET.get('q')
    if q:
        productos_lista = Producto.objects.filter(nombre__icontains=q)
    else:
        productos_lista = Producto.objects.all()
    context = {'productos_lista': productos_lista}
    return render(request, "productos/productos_lista.html", context)


def productos_form(request,id=0):
    if request.method == "GET":
        if id ==0:
            form = ProductosForm()
        else:
            producto = Producto.objects.get(pk=id)
            form = ProductosForm(instance=producto)
        return render(request,"productos/productos_form.html",{'form':form})
    else:
        if id ==0 :
            form = ProductosForm(request.POST)
        else:
            producto = Producto.objects.get(pk=id)
            form = ProductosForm(request.POST,instance=producto)
        if form.is_valid():
            form.save()
        return redirect('/productos/list')

def productos_eliminar(request,id):
    producto = Producto.objects.get(pk=id)
    producto.delete()
    return redirect('/productos/list')

def productos_read(request, id):
    producto = Producto.objects.get(pk=id)
    context = {'producto': producto}
    return render(request, "productos/productos_read.html", context)

from django.conf import settings
from django.utils import timezone
from pytz import timezone as pytz_timezone

def generar_reporte_pdf(request):
    time_zone = pytz_timezone(settings.TIME_ZONE)  # Obtiene el objeto de zona horaria
    productos_lista = Producto.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(100, 750, "Reportes EcoFácil")
    fecha_actual = timezone.now().astimezone(time_zone).strftime("%d/%m/%Y %H:%M:%S")
    pdf.setFont('Helvetica', 10)
    pdf.drawString(380, 750, f"Fecha del reporte: {fecha_actual}")
    y = 700
    x = 50
    pdf.setFont('Helvetica-Bold', 12)
    pdf.drawString(x, y, "Reporte de Productos")
    pdf.setFont('Helvetica', 12)
    y -= 22
    pdf.drawString(x, y, "Nombre:")
    pdf.drawString(x + 90, y, "Material:")
    pdf.drawString(x + 200, y, "Cantidad:")
    pdf.drawString(x + 330, y, "Precio:")
    pdf.drawString(x + 430, y, "Categoría:")
    y -= 18

    for producto in productos_lista:
        pdf.drawString(x, y, producto.nombre)
        pdf.drawString(x + 90, y, producto.material)
        pdf.drawString(x + 215, y, str(producto.cantidad))
        pdf.drawString(x + 335, y, str(producto.precio))
        pdf.drawString(x + 430, y, str(producto.categoria))
        y -= 14
    pdf.showPage()
    pdf.save()

    request.session['redirigir_despues_de_descargar'] = True
    
    return response

