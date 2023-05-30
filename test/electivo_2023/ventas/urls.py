from django.urls import path,include
from . import views

urlpatterns = [
    
    path('crear_orden_venta/',views.crear_orden_venta,name="crear_orden_venta"),
    path('ver_orden_venta/<int:id>/',views.ver_orden_venta,name="ver_orden_venta"),
    path('listar_orden_venta/',views.listar_orden_venta,name="listar_orden_venta"),
    #path('',views.orden_venta_main,name='orden_venta_main'),
    path('orden_venta_edit/<int:id>/', views.crear_orden_venta,name='orden_venta_edit'),
    
    path('ver_orden_venta/<int:id>/',views.ver_orden_venta,name="ver_orden_venta"),
    path('eliminar_orden_venta/<int:id>/',views.eliminar_orden_venta,name="eliminar_orden_venta"),
    path('eliminar_detalle_venta/<int:id>/',views.eliminar_detalle_venta,name="eliminar_detalle_venta"),
    path('orden_venta_main',views.orden_venta_main,name='orden_venta_main'),
    path('generar_pdfventa/', views.generar_pdfventa, name='generar_pdfventa'),
    
    
    
]
