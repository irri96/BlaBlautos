from django.shortcuts import render,redirect
from Nucleo.models import Viaje,Tramo,Reservacion
from datetime import datetime,timedelta
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


def CancelarReserva(request, reserva):
    res = Reservacion.objects.get(id=reserva)
    if res.estado_reserva==Reservacion.ACEPTADO:
        for tramo in res.tramos.all():
            tramo.asientos_libres+=1
            tramo.save()
    res.delete()
    return redirect('/')


def Confirmar(request, reserva):
    print("reserva a cancelar ",reserva)
    return render(request, 'confirmacion.html', {"reserva":Reservacion.objects.get(id=reserva),'mensaje':'¿Está seguro que desea eliminar su reserva?'})

