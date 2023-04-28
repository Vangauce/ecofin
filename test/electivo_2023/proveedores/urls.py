from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.proveedores_form,name='proveedores_insert'), # get and post req. for insert operation
    path('<int:id>/', views.proveedores_form,name='proveedores_update'), # get and post req. for update operation
    path('read/<int:id>/', views.proveedores_read,name='proveedores_read'),
    path('delete/<int:id>/',views.proveedores_eliminar,name='proveedores_delete'),
    path('list/',views.proveedores_lista,name='proveedores_list'), # get req. to retrieve and display all records
]