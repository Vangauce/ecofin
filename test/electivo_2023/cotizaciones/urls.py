from django.urls import path
from .views import crear_cotizacion
from .views import detalle_cotizacion, listado_cotizacion, borrar_cotizacion,editar_cotizacion,generar_reporte
from . import views

urlpatterns = [
    path('crear/', crear_cotizacion, name='crear_cotizacion'),
    path('detalle/<int:cotizacion_id>/', detalle_cotizacion, name='detalle_cotizacion'),
    path('listado_cotizacion/', listado_cotizacion, name='listado_cotizacion'),
    path('borrar/<int:cotizacion_id>/', borrar_cotizacion, name='borrar_cotizacion'),
    path('editar/<int:cotizacion_id>/', editar_cotizacion, name='editar_cotizacion'),
    path('generar-reporte/', generar_reporte, name='generar_reporte'),
    path('',views.cotizaciones_main,name='cotizaciones_main'),
    path('generar_reporte_pdf/<int:cotizacion_id>/', views.generar_reporte_pdf, name='generar_reporte_pdf'),
    path('ruta/', views.generar_reporte_general_pdf, name='generar_reporte_general_pdf'),

]
