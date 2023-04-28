from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductosForm


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




