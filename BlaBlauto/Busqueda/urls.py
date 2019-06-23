from django.urls import include, path

from Busqueda.views import Buscar, BuscarList
from django.contrib import admin

urlpatterns = [
    path('buscar/',Buscar,name='Buscar'),
    path('buscar/listar',BuscarList.as_view(),name='ListarBusqueda'),
]
