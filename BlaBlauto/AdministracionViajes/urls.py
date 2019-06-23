from django.urls import include, path

from AdministracionViajes.views.creacionviaje import *
from AdministracionViajes.views.administrarviaje import *
from AdministracionViajes.views.cancelacionviaje import *
from AdministracionViajes.views.vistaviaje import *

from django.contrib import admin

urlpatterns = [
    path('crear/',crear,name='CrearViaje'),

    path(r'iniciar_viaje/', IniciarViaje, name="iniciar_viaje"),
    path(r'administrar_viaje/<int:id_viaje>/', AdministrarViaje, name="administrar_viaje"),

    path(r'cancelarviaje/<int:id>/', CancelarViaje, name="cancelar_viaje"),
    path(r'cancelarviaje/confirmar/<int:id>/', ConfirmarCancelacion, name="confirmar_cancelar_viaje"),

    path(r'listarviajes/', VerViajes, name="listarviajes"),
    path(r'viaje/<int:id>/', VerViaje, name="viaje")

]
