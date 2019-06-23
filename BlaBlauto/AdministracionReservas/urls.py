from django.urls import include, path

from AdministracionReservas.views.administrarreservas import *
from AdministracionReservas.views.cancelarreserva import *
from AdministracionReservas.views.reservarviaje import *
from AdministracionReservas.views.reservaschofer import VerReservas as VerReservasChofer,VerReservantes
from AdministracionReservas.views.reservaspasajero import *

from django.contrib import admin

urlpatterns = [

    path(r'mis_reservas/', VerReservas , name="mis_reservas"),
    path(r'cancelar/<int:inicio>/<int:fin>/', CancelarReserva, name="cancelar"),
    path(r'cancelar/<int:reserva>/', CancelarReserva, name="cancelar_reserva"),
    path(r'confirmar/<int:reserva>/', Confirmar, name="confirmar"),
    path(r'reservasviaje/<int:id>/', VerReservasChofer, name="ver_reservas_viaje"),
    path(r'reservasviaje/aceptar/<int:id>/', AceptarReserva, name="aceptar_reserva"),
    path(r'reservasviaje/confirmar/aceptar/<int:id>/', ConfirmarAceptacion, name="confirmar_aceptar"),
    path(r'reservasviaje/confirmar/rechazar/<int:id>/', ConfirmarRechazo, name="confirmar_rechazar"),
    path(r'reservasviaje/rechazar/<int:id>/', RechazarReserva, name="rechazar_reserva"),
    path('reservar/<int:pk>/<str:origen>/<str:destino>',reservar,name='ReservarViaje'),
    path(r'reservantes/<int:id>/', VerReservantes, name="ver_reservantes"),

]
