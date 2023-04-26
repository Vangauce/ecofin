from django.shortcuts import render, redirect
from .models import Insumos
from .forms import InsumosForm


def insumos_lista(request):
    context = {'insumos_lista': Insumos.objects.all()}
    return render(request,"insumos/insumos_lista.html",context)

def insumos_form(request,id=0):
    if request.method == "GET":
        if id ==0:
            form = InsumosForm()
        else:
            insumos = Insumos.objects.get(pk=id)
            form = InsumosForm(instance=insumos)
        return render(request,"insumos/insumos_form.html",{'form':form})
    else:
        if id ==0 :
            form = InsumosForm(request.POST)
        else:
            insumos = Insumos.objects.get(pk=id)
            form = InsumosForm(request.POST,instance=insumos)
        if form.is_valid():
            form.save()
        return redirect('/insumos/list')

def insumos_eliminar(request,id):
    insumos = Insumos.objects.get(pk=id)
    insumos.delete()
    return redirect('/insumos/list')

def insumos_read(request, id):
    insumos = Insumos.objects.get(pk=id)
    context = {'insumos': insumos}
    return render(request, "insumos/insumos_read.html", context)
