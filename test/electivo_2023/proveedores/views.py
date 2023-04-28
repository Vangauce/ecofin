from django.shortcuts import render, redirect
from .models import Proveedores
from .forms import ProveedoresForm

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