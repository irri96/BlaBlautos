from django.shortcuts import render,redirect
from Nucleo.models import Viaje,Tramo,Reservacion,Chofer,User
from datetime import datetime,timedelta
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


def VerReservas(request,id):
    try:
        chofer = Chofer.objects.get(user=User(id=request.user.id))
    except:
        return render(request, 'error.html', {"mensaje": "No has ingresado al sistema como chofer", "redirection":"/"})
    try:
        viaje = Viaje.objects.get(id=id)
    except:
        return render(request, 'error.html', {"mensaje": "El viaje no existe",
                                              "redirection": "/"})
    elset = set([])
    for tramo in viaje.tramos.all():
        for reserva in tramo.reservas_del_tramo.all():
            elset.add(reserva)
    if viaje.conductor!=chofer:
        return render(request, 'error.html', {"mensaje": "No estás autorizado para mirar este viaje",
                                              "redirection": "/"})
    return render(request,'reservasviaje.html',{"reservas":list(elset)})


def VerReservantes(request,id):
    try:
        chofer = Chofer.objects.get(user=User(id=request.user.id))
    except:
        return render(request, 'error.html', {"mensaje": "No has ingresado al sistema como chofer", "redirection":"/"})
    try:
        viaje = Viaje.objects.get(id=id)
    except:
        return render(request, 'error.html', {"mensaje": "El viaje no existe",
                                              "redirection": "/"})
    elset = set([])
    for tramo in viaje.tramos.all():
        for reserva in tramo.reservas_del_tramo.all():
            if reserva.estado_reserva == 2:
                elset.add(reserva.pasajero)
    if viaje.conductor!=chofer:
        return render(request, 'error.html', {"mensaje": "No estás autorizado para mirar este viaje",
                                              "redirection": "/"})
    return render(request,'reservantes.html',{"pasajeros":list(elset)})