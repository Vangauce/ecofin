from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.categorias_form,name='categorias_insert'), # get and post req. for insert operation
    path('<int:id>/', views.categorias_form,name='categorias_update'), # get and post req. for update operation
    path('read/<int:id>/', views.categorias_read,name='categorias_read'),
    path('delete/<int:id>/',views.categorias_eliminar,name='categorias_delete'),
    path('list/',views.categorias_lista,name='categorias_list') # get req. to retrieve and display all records
]