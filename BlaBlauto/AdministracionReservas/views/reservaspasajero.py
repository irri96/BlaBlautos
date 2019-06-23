from django.shortcuts import render,redirect
from Nucleo.models import Viaje,Tramo,Reservacion,Pasajero,User
from datetime import datetime,timedelta
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

def VerReservas(request):
    p = Pasajero.objects.get(user=User(id=request.user.id))
    lista = []
    for reserva in Reservacion.objects.filter(pasajero=p):
        first = reserva.tramos.first()
        second = reserva.tramos.last()
        lista.append((first,second,reserva.estado_pago,reserva.estado_reserva,reserva))
    return render(request, 'reservas.html', {"lista":lista})

