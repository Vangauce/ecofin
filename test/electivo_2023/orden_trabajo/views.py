from django.shortcuts import render

# Create your views here.
def orden_trabajo_main(request):
    return render(request, 'orden_trabajo/orden_trabajo_main.html')