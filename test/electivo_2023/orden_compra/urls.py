from django.urls import path
from .views import crear_orden_compra ,detalle_orden_compra, listado_orden_compra, borrar_orden_compra, editar_orden_compra
from . import views

urlpatterns = [
path('crear/', crear_orden_compra, name='crear_orden_compra'),
path('detalle/<int:orden_compra_id>/', detalle_orden_compra, name='detalle_orden_compra'),
path('listado_orden_compra/', listado_orden_compra, name='listado_ordenes_compra'),
path('borrar/<int:orden_compra_id>/', borrar_orden_compra, name='borrar_orden_compra'),
path('editar/<int:orden_compra_id>/', editar_orden_compra, name='editar_orden_compra'),
path('generar-reporte/', views.generar_reporte_orden_compra, name='generar_reporte_orden_compra'),
path('', views.ordenes_compra_main, name='orden_compra_main'),
]