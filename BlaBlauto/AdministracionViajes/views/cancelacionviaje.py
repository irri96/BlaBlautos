from django.shortcuts import render
from Nucleo.models import Chofer,Viaje,User
# Create your views here.

def CancelarViaje(request,id):
    print("cancelo",id)
    try:
        chofer = Chofer.objects.get(user=User(id=request.user.id))
        viaje = Viaje.objects.get(id=id)
        viajes = Viaje.objects.filter(conductor=chofer)
        if viaje.conductor!=chofer:
            return render(request, 'listarviajes.html', {"viajes": viajes, "mensaje":
                "No estás autorizado a realizar esa acción"})
        viaje.limpiar_reservas()
        viaje.delete()
        return render(request, 'listarviajes.html', {"viajes": viajes,"mensaje":"Viaje eliminado exitosamente"})
    except Viaje.DoesNotExist:
        viajes = Viaje.objects.filter(conductor=chofer)
        return render(request, 'listarviajes.html', {"viajes": viajes,"mensaje":"El viaje no existe"})

def ConfirmarCancelacion(request,id):
    try:
        viaje = Viaje.objects.get(id=id)
    except Viaje.DoesNotExist:
        return render(request, 'error.html',
                      {"mensaje": "El viaje no existe",
                       "redirection": "/listarviajes/"})
    try:
        chofer = Chofer.objects.get(user=User(id=request.user.id))
    except Chofer.DoesNotExist:
        return render(request, 'error.html',
                      {"mensaje": "No has ingresado al sistema como conductor",
                       "redirection": "/"})
    chofer_viaje = Chofer.objects.get(user=User(id=viaje.conductor.id))
    if chofer!=chofer_viaje:
        return render(request, 'error.html',
                      {"mensaje": "No tienes permiso para realizar esta acción",
                       "redirection": "/listarviajes/"})
    return render(request, 'confirmacion.html', {"viaje_cancelado": viaje})

