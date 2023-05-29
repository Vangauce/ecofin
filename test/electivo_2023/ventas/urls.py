from django.urls import path,include
from . import views

urlpatterns = [
    
    path('crear_orden_venta/',views.crear_orden_venta,name="crear_orden_venta"),
    path('ver_orden_venta/<int:id>/',views.ver_orden_venta,name="ver_orden_venta"),
    path('listar_orden_venta/',views.listar_orden_venta,name="listar_orden_venta"),
    
    
]