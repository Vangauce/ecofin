from django.shortcuts import render, redirect
from .models import Categorias
from .forms import CategoriasForm


def categorias_lista(request):
    context = {'categorias_lista': Categorias.objects.all()}
    return render(request,"categorias/categorias_lista.html",context)

def categorias_form(request,id=0):
    if request.method == "GET":
        if id ==0:
            form = CategoriasForm()
        else:
            categorias = Categorias.objects.get(pk=id)
            form = CategoriasForm(instance=categorias)
        return render(request,"categorias/categorias_form.html",{'form':form})
    else:
        if id ==0 :
            form = CategoriasForm(request.POST)
        else:
            categorias = Categorias.objects.get(pk=id)
            form = CategoriasForm(request.POST,instance=categorias)
        if form.is_valid():
            form.save()
        return redirect('/categorias/list')

def categorias_eliminar(request,id):
    categorias = Categorias.objects.get(pk=id)
    categorias.delete()
    return redirect('/categorias/list')

def categorias_read(request, id):
    categorias = Categorias.objects.get(pk=id)
    context = {'categorias': categorias}
    return render(request, "categorias/categorias_read.html", context)

