from django.urls import path,include
from . import views

urlpatterns = [

    path('',views.orden_trabajo_main,name='orden_trabajo_main'),

    
]