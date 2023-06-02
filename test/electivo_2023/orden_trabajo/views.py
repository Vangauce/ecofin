from django.shortcuts import render, get_object_or_404, redirect
from ventas.models import Ventas, Detalle_orden_venta


def orden_trabajo_main(request):
    return render(request, 'orden_trabajo/orden_trabajo_main.html')


def listar_ventas(request):
    ventas = Ventas.objects.all()
    detalles = Detalle_orden_venta.objects.filter(venta__in=ventas)
    return render(request, 'orden_trabajo/listar_ventas.html', {'ventas': ventas, 'detalles': detalles})


def ver_estado_venta(request, id):
    venta = Ventas.objects.get(pk=id)
    ventas = [venta]  # Convertir la instancia en una lista de un solo elemento
    context = {'ventas': ventas}
    return render(request, 'orden_trabajo/ver_estado_venta.html', context)

def cambiar_estado_venta(request, id):
    venta = get_object_or_404(Ventas, pk=id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        venta.estado = nuevo_estado
        venta.save()
        return redirect('listar_ventas') 

    context = {'venta': venta}
    return render(request, 'orden_trabajo/cambiar_estado_venta.html', context)

