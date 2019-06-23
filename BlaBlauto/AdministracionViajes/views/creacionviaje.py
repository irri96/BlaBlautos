def crear(request):
	viaje = CrearForm() # se asigna formulario de viajes
	if request.method == 'POST':
		ok=True
		viaje = CrearForm(request.POST or None)
		if viaje.is_valid(): viaje = viaje.cleaned_data #ver si está bien llenado
		paradas = []
		horas = {}
		# else return error
		for k, v in request.POST.items():
			if k=="ciudad_origen":
				ciudad_origen = v
				paradas.append((1,v))
			elif k=="ciudad_destino":
				ciudad_destino = v
				paradas.append((9999,v))
			elif k=="tiempo_inicio":
				tiempo = datetime.strptime(v, "%Y-%m-%dT%H:%M")
				horas[1]=tiempo
				pass
			elif k=="asientos":
				asientos = int(v)
				pass
			elif k=="tiempo_final":
				tiempo = datetime.strptime(v, "%Y-%m-%dT%H:%M")
				horas[9999]=tiempo
			elif k=="csrfmiddlewaretoken":
				pass
			elif k.startswith("lugar"):
				num = int(k[5:])
				paradas.append((num, v))
			elif k.startswith("hora"):
				num = int(k[4:])
				tiempo = datetime.strptime(v, "%Y-%m-%dT%H:%M")
				horas[num]=tiempo

			print(k,v) # k es el nombre que se le da en el html a los inputs, v son los valores que me devuelve el rellenado del form
		print(paradas)
		paradas.sort()
		print(paradas)
		elchofer = request.user.chofer
		print("antes",Viaje.objects.all())
		miviaje = Viaje(conductor=elchofer,tiempo_inicio=horas[1],asientos=asientos,ciudad_origen=ciudad_origen,
						ciudad_destino=ciudad_destino,realizado=False)
		miviaje.save()
		for i in range(0,len(paradas)-1):
			k1 = paradas[i][0]
			k2 = paradas[i+1][0]
			#print(paradas[i][1],paradas[i+1][1],tiempo_inicio+timedelta(hours=i))
			origen = paradas[i][1]
			destino = paradas[i+1][1]
			hora_inicio = horas[k1]
			hora_final = horas[k2]
			if hora_final<hora_inicio:
				print("error menor")
				miviaje.delete()
				ok=False
				break
			tramo = Tramo(viaje=miviaje,hora_inicio=hora_inicio,hora_final=hora_final,precio=100,
						  asientos_libres=asientos,ciudad_origen=origen,ciudad_destino=destino)
			tramo.save()
		print("despues", Viaje.objects.all())
		if ok:
			return redirect('/listarviajes')
		else:
			return render(request, 'form_crear.html', {'form': viaje})
	return render(request, 'form_crear.html', {'form': viaje})