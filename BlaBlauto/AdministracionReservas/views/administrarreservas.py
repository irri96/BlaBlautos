from django.shortcuts import render,redirect
from Nucleo.models import Viaje,Tramo,Reservacion,Chofer,User
from datetime import datetime,timedelta
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
# Create your views here.

@transaction.atomic
def RechazarReserva(request,id):
    print("rechazo",id)
    try:
        chofer = Chofer.objects.get(user=User(id=request.user.id))
        reserva = Reservacion.objects.get(id=id)
    except Chofer.DoesNotExist:
        return render(request, 'error.html',
                      {"mensaje": "No estás loggeado como conductor",
                       "redirection": "/"})
    except Reservacion.DoesNotExist:
        return render(request, 'error.html',
                      {"mensaje": "La reserva no existe",
                       "redirection": "/"})
    conductor_reserva = reserva.tramos.first().viaje.conductor
    if conductor_reserva != chofer:
        return render(request, 'error.html',
                      {"mensaje": "No tienes permiso para realizar esta acción",
                       "redirection": "/listarviajes/"})
    if reserva.estado_reserva==Reservacion.ACEPTADO:
        for tramo in reserva.tramos.all():
            tramo.asientos_libres=tramo.asientos_libres+1
            tramo.save()
    elif reserva.estado_reserva==Reservacion.RECHAZADO:
        return render(request, 'error.html',
                      {"mensaje": "La reserva ya fue rechazada anteriormente",
                       "redirection": "/reservasviaje/" + str(reserva.tramos.first().viaje.id)})
    reserva.estado_reserva=Reservacion.RECHAZADO
    reserva.save()
    viaje = Viaje.objects.get(id=reserva.tramos.first().viaje.id)
    elset = set([])
    for tramo in viaje.tramos.all():
        for reserva in tramo.reservas_del_tramo.all():
            elset.add(reserva)
    print(viaje.id)
    return render(request, 'reservasviaje.html', {"mensaje": "Reserva rechazada", "reservas": list(elset)})

@transaction.atomic
def AceptarReserva(request,id):
    print("acepto",id)
    try:
        chofer = Chofer.objects.get(user=User(id=request.user.id))
        reserva = Reservacion.objects.get(id=id)
    except Chofer.DoesNotExist:
        return render(request, 'error.html',
                      {"mensaje": "No estás loggeado como conductor",
                       "redirection": "/" })
    except Reservacion.DoesNotExist:
        return render(request, 'error.html',
                      {"mensaje": "La reserva no existe",
                       "redirection": "/"})
    conductor_reserva = reserva.tramos.first().viaje.conductor
    if conductor_reserva != chofer:
        return render(request, 'error.html',
                      {"mensaje": "No tienes permiso para realizar esta acción",
                       "redirection": "/listarviajes/" })
    tramos = reserva.tramos
    capacidad = True
    mensaje="Reserva aceptada"
    if reserva.estado_reserva!=Reservacion.ACEPTADO:
        for tramo in tramos.all():
            if tramo.asientos_libres<=0:
                capacidad=False
        if capacidad:
            for tramo in tramos.all():
                tramo.asientos_libres=tramo.asientos_libres-1
                tramo.save()
            reserva.estado_reserva=Reservacion.ACEPTADO
            reserva.save()
        else:
            mensaje="No hay suficientes cupos disponibles"
            return render(request,'error.html',
                          {"mensaje":"No hay suficientes cupos disponibles",
                           "redirection":"/reservasviaje/"+str(reserva.tramos.first().viaje.id)})

    else:
        return render(request, 'error.html',
                      {"mensaje": "La reserva ya fue aceptada anterioemente",
                       "redirection": "/reservasviaje/" + str(reserva.tramos.first().viaje.id)})
    viaje = Viaje.objects.get(id=reserva.tramos.first().viaje.id)
    elset = set([])
    for tramo in viaje.tramos.all():
        for reserva in tramo.reservas_del_tramo.all():
            elset.add(reserva)

    return render(request,'reservasviaje.html',{"mensaje":mensaje,"reservas":list(elset)})

def ConfirmarAceptacion(request,id):
    try:
        chofer = Chofer.objects.get(user=User(id=request.user.id))
        reserva = Reservacion.objects.get(id=id)
    except Chofer.DoesNotExist:
        return render(request, 'error.html', {"mensaje": "No has ingresado al sistema como chofer",
                                              "redirection": "/"})
    except Reservacion.DoesNotExist:
        return render(request, 'error.html', {"mensaje": "Acción no autorizada",
                                              "redirection": "/listarviajes"})
    conductor_reserva = reserva.tramos.first().viaje.conductor
    if conductor_reserva != chofer:
        return render(request, 'error.html', {"mensaje": "Acción no autorizada",
                                              "redirection": "/listarviajes"})
    return render(request,'confirmacion.html',{"reserva_aceptada":reserva})

def ConfirmarRechazo(request,id):
    try:
        chofer = Chofer.objects.get(user=User(id=request.user.id))
        reserva = Reservacion.objects.get(id=id)
    except Chofer.DoesNotExist:
        return render(request, 'error.html',
                      {"mensaje": "No estás loggeado como conductor",
                       "redirection": "/"})
    except Reservacion.DoesNotExist:
        return render(request, 'error.html',
                      {"mensaje": "La reserva no existe",
                       "redirection": "/"})
    conductor_reserva = reserva.tramos.first().viaje.conductor
    if conductor_reserva != chofer:
        return render(request, 'error.html',
                      {"mensaje": "No tienes permiso para realizar esta acción",
                       "redirection": "/listarviajes/"})
    return render(request,'confirmacion.html',{"reserva_rechazada":reserva})