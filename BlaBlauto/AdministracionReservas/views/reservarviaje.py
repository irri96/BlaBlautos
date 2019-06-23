from django.shortcuts import render,redirect
from Nucleo.models import Viaje,Tramo,Reservacion
from datetime import datetime,timedelta
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


@user_passes_test(lambda u: u.es_pasajero)
def reservar(request,pk,origen,destino):
	print(pk,origen,destino)
	pasajero = request.user.pasajero
	viaje = Viaje.objects.all().get(pk=pk)
	hora_inicio= Tramo.objects.all().filter(viaje=viaje).get(ciudad_origen=origen).hora_inicio
	hora_final= Tramo.objects.all().filter(viaje=viaje).get(ciudad_destino=destino)
	tramos = Tramo.objects.filter(viaje=viaje).filter(hora_inicio__range=(hora_inicio, hora_final.hora_inicio))
	print("tramos! ", tramos)
	reserva = Reservacion(pasajero=pasajero,asientos=1,estado_pago=False)
	reserva.save()
	for tramo in tramos:
		reserva.tramos.add(tramo)
		tramo.save()

	reserva.save()

	print(tramos)
	#tramo_destino= Viaje.objects.all().filter(pk=pk).filter(tramos__ciudad_destino=destino)

	return redirect('/')


