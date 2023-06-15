from django.urls import path,include
from . import views

urlpatterns = [

    path('insert', views.ordentrabajo_form, name= 'ordentrabajo_insert'),
    path('<int:id>/', views.ordentrabajo_form,name='ordentrabajo_update'),
    path('read/<int:id>', views.ordentrabajo_read, name='ordentrabajo_read'),
    path('delete/<int:id>', views.ordentrabajo_eliminar, name='ordentrabajo_delete'),
    path('delete1/<int:id>', views.ordentrabajo_eliminar1, name='ordentrabajo_delete1'),
    path('list/', views.ordentrabajo_lista, name='ordentrabajo_list'),
    path('',views.orden_trabajo_main,name='orden_trabajo_main'),
    path('carga_masiva_ordentrabajo/',views.carga_masiva_ordentrabajo,name='carga_masiva_ordentrabajo'),
    path('import_file_ordentrabajo/',views.import_file_ordentrabajo,name="import_file_ordentrabajo"),
    path('carga_masiva_ordentrabajo_save/',views.carga_masiva_ordentrabajo_save,name="carga_masiva_ordentrabajo_save"),
    
    path('listar_ventas',views.listar_ventas,name='listar_ventas'),
    path('ver_estado_venta/<int:id>/',views.ver_estado_venta,name='ver_estado_venta'),
    path('cambiar_estado_venta/<int:id>/',views.cambiar_estado_venta,name='cambiar_estado_venta'),

    path('reporte_pdf/',views.generar_reporte_pdf, name='reporte_pdf')
    
]