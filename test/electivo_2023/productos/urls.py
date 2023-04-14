from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.productos_form,name='productos_insert'), # get and post req. for insert operation
    path('<int:id>/', views.productos_form,name='productos_update'), # get and post req. for update operation
    path('delete/<int:id>/',views.productos_eliminar,name='productos_delete'),
    path('list/',views.productos_lista,name='productos_list') # get req. to retrieve and display all records
]