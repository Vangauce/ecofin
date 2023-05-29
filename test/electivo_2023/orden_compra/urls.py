from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.orden_compra_main,name='orden_compra_main'),
    path('crear_orden/',views.crear_orden,name="crear_orden"),
    path('orden_edit/<int:id>/', views.crear_orden,name='orden_edit'),
    path('ver_orden_compra/<int:id>/',views.ver_orden_compra,name="ver_orden_compra"),
    path('eliminar_orden_compra/<int:id>/',views.eliminar_orden_compra,name="eliminar_orden_compra"),
    path('eliminar_detalle/<int:id>/',views.eliminar_detalle,name="eliminar_detalle"),
    path('listar_orden_compra/',views.listar_orden_compra,name="listar_orden_compra"),
    path('generar_pdf1/', views.generar_pdf1, name='generar_pdf1'),

    
]