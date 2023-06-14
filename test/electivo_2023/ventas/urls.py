from django.urls import path,include
from . import views

urlpatterns = [
    
    path('crear_orden_venta/',views.crear_orden_venta,name="crear_orden_venta"),
    path('listar_orden_venta/',views.listar_orden_venta,name="listar_orden_venta"),
    path('detalle/<int:orden_venta_id>/', views.detalle_orden_venta, name='detalle_orden_venta'),
    path('eliminar_orden_venta/<orden_venta_id>/',views.borrar_orden_venta,name="borrar_orden_venta"),
    path('eliminar_detalle_venta/<int:id>/',views.eliminar_detalle_venta,name="eliminar_detalle_venta"),
    path('editar/<int:orden_venta_id>/', views.editar_orden_venta, name='editar_orden_venta'),
    path('orden_venta_main',views.orden_venta_main,name='orden_venta_main'),
    path('generar_pdfventa/', views.generar_pdfventa, name='generar_pdfventa'),
    
    
    
]
