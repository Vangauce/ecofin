from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.orden_trabajo_main,name='orden_trabajo_main'),
    path('listar_ventas',views.listar_ventas,name='listar_ventas'),
    path('ver_estado_venta/<int:id>/',views.ver_estado_venta,name='ver_estado_venta'),
    path('cambiar_estado_venta/<int:id>/',views.cambiar_estado_venta,name='cambiar_estado_venta'),

    
]