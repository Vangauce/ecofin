from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.orden_trabajo_main,name='orden_trabajo_main'),
    path('listar_ventas',views.listar_ventas,name='listar_ventas'),
    path('ver_estado_venta/<int:id>/',views.ver_estado_venta,name='ver_estado_venta'),
    path('cambiar_estado_venta/<int:id>/',views.cambiar_estado_venta,name='cambiar_estado_venta'),
    path('estado_venta/crear/', views.crear_estado_venta, name='crear_estado_venta'),
    path('venta/<int:venta_id>/asignar_estado/', views.asignar_estado_venta, name='asignar_estado_venta'),

    
]