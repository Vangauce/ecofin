from django.shortcuts import render, redirect
from .models import Insumos
from .forms import InsumosForm


def insumos_main(request):
    total_insumos = Insumos.total_insumos()
    return render(request, 'insumos/insumos_main.html', {'total_insumos': total_insumos})

def insumos_lista(request):
    q = request.GET.get('q')
    if q:
        insumos_lista = Insumos.objects.filter(nombre__icontains=q)
    else:
        insumos_lista = Insumos.objects.all()
    context = {'insumos_lista': insumos_lista}
    return render(request, "insumos/insumos_lista.html", context)

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


def insumos_dashboard(request):
    context = {'insumos': Insumos.objects.all()}
    return render(request, "insumos/dashboard.html", context)
