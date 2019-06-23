from Nucleo.models import *
from django.shortcuts import render,redirect


def VerViajes(request):
    try:
        chofer = Chofer.objects.get(user=User(id=request.user.id))
        viajes = Viaje.objects.filter(conductor=chofer)
    except Chofer.DoesNotExist:
        return render(request, 'error.html', {"mensaje": "No has ingresado al sistema como chofer", "redirection":"/"})
    return render(request, 'listarviajes.html', {"viajes": viajes})


def VerViaje(request,id):
    try:
        pasajero = Pasajero.objects.get(user=User(id=request.user.id))
    except Pasajero.DoesNotExist:
        try:
            chofer = Chofer.objects.get(user=User(id=request.user.id))
        except Chofer.DoesNotExist:
            return redirect("/")

    viaje = Viaje.objects.get(id=id)
    elset = set([])
    for tramo in viaje.tramos.all():
        elset.add(tramo)
    return render(request, 'verviaje.html',{"viaje": viaje, "tramos":list(elset)})