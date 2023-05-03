from django.urls import path,include
from . import views

urlpatterns = [
    path('insert', views.productos_form,name='productos_insert'), # get and post req. for insert operation
    path('<int:id>/', views.productos_form,name='productos_update'), # get and post req. for update operation
    path('read/<int:id>/', views.productos_read,name='productos_read'),
    path('delete/<int:id>/',views.productos_eliminar,name='productos_delete'),
    path('list/',views.productos_lista,name='productos_list'), # get req. to retrieve and display all records
    path('',views.productos_main,name='productos_main'),
]