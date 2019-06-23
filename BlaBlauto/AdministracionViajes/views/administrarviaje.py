from django.shortcuts import render,redirect
from AdministracionViajes.forms import CrearForm
from Nucleo.models import Viaje,Tramo,Reservacion
from datetime import datetime,timedelta
from django.contrib.auth.decorators import user_passes_test
from Nucleo.models import *
# Create your views here.


@user_passes_test(lambda u: u.es_chofer)
def IniciarViaje(request):
	if request.method == "POST":
		for key, value in request.POST.items():
			if "csrf" in key: continue
			print(key,value)
			return render(request, 'confirmacion.html', {'viaje':Viaje.objects.get(id=int(key)),'mensaje':'¿Desea iniciar su viaje?'})
	hoy = datetime.today()
	chofer = request.user.chofer
	viajes = []
	tramos = []
	viaje_activo = False
	if Viaje.objects.filter(conductor=chofer,en_curso=True,realizado=False).exists():
		viaje = Viaje.objects.get(conductor=chofer,en_curso=True,realizado=False)
		for t in Tramo.objects.filter(viaje=viaje):
			tramos.append(t)
		viajes.append((viaje, tramos))
		viaje_activo = True
	for viaje in Viaje.objects.filter(conductor=chofer,tiempo_inicio__day=hoy.day,tiempo_inicio__month=hoy.month,tiempo_inicio__year=hoy.year,realizado=False,en_curso=False):
		for tramo in Tramo.objects.filter(viaje=viaje):
			tramos.append(tramo)
		viajes.append((viaje,tramos))
	viajes_futuros = []
	for viaje in Viaje.objects.filter(conductor=chofer, realizado=False,tiempo_inicio__gte=hoy+timedelta(1)):
		viajes_futuros.append(viaje)
	return render(request, 'iniciar_viaje.html', {'viajes':viajes, 'futuros':viajes_futuros, 'en_viaje':viaje_activo})

@user_passes_test(lambda u: u.es_chofer)
def AdministrarViaje(request, id_viaje):
	try:
		viaje = Viaje.objects.get(id=id_viaje)
		chofer = Chofer.objects.get(user=User.objects.get(id=request.user.id))
		if viaje.conductor != chofer:return render(request, 'inicio.html', {'mensaje':'Usted no puede ingresar a este viaje'})
		if viaje.realizado: return render(request, 'inicio.html', {'mensaje':'El viaje al que intenta ingresar ya finalizó'})
		viaje.en_curso = True
		viaje.save()
		tramos = []
		reservas = set()
		t = list(viaje.tramos.all())
		reservas_totales = set()
		for tramo in t:
			r = []
			bajada = []
			for reserva in Reservacion.objects.filter(tramos=tramo.id, estado_reserva=2):
				reservas_totales.add(reserva)
				tramitos = reserva.tramos.all()
				if tramo == tramitos[len(tramitos)-1]:bajada.append((reserva, tramo))
				if reserva not in reservas:
					r.append(reserva)
					reservas.add(reserva)
			tramos.append((tramo, r, bajada))
		if request.method == "POST":
			if len(request.POST)-1 != len(reservas_totales):
				return render(request, 'administrar_viaje.html', {'tramos': tramos, 'ERROR':'Indique si todos sus pasajeros se subieron'})
			for key, value in request.POST.items():
				if 'csrf' in key or value == 'no': continue
				r = Reservacion.objects.get(id=int(key))
				r.realizado = True
				r.save()
			viaje.realizado = True
			viaje.en_curso = False
			viaje.save()
			return render(request, 'inicio.html', {'mensaje':'Su viaje finalizó exitosamente'})
		return render(request, 'administrar_viaje.html', {'tramos':tramos})
	except Viaje.DoesNotExist:
		return redirect('/')