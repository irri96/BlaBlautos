from django.shortcuts import render

# Create your views here.
from .forms import BuscarViajeForm
from django.db.models import Q,F
from django.db.models.expressions import RawSQL
from Nucleo.models import Viaje
from django.http import HttpResponseRedirect
from django.views.generic import ListView
class BuscarList(ListView):
    model = Viaje
    template_name = "classroom/buscar/listarbusqueda.html"
    def get_queryset(self):
        origen =self.request.GET.get('origen')
        destino = self.request.GET.get('destino')
        fecha = self.request.GET.get('fecha')
        print(fecha)
        viajes = Viaje.objects.all().filter(tiempo_inicio__date=fecha, realizado=False)
        borrar = []
        for v in viajes:
            if not v.tramos.filter(ciudad_origen=origen).exists() and not v.tramos.filter(ciudad_destino=destino).exists():
                borrar.append(v.pk)
        for pk in borrar:
            viajes=viajes.exclude(pk=pk)

        return viajes.filter(tramos__ciudad_origen=origen).annotate(lahora = F('tramos__hora_inicio')).annotate(
            mi_origen=RawSQL("SELECT '%s'"%(origen,), ())).annotate(mi_destino=RawSQL("SELECT '%s'"%(destino,), ()))


def Buscar(request):
    form = BuscarViajeForm(request.POST)
    if request.method == "POST"  and form.is_valid():
        origen = form.cleaned_data['ciudad_origen']
        destino = form.cleaned_data['ciudad_destino']
        fecha = form.cleaned_data['fecha']
        viajes = Viaje.objects.all()
        existio = False

        for v in viajes:
            if v.tramos.filter(Q(ciudad_origen=origen)|Q(ciudad_destino=destino)).count()==2:
                existio=True
                break
        return HttpResponseRedirect('/buscar/listar?origen=%s&destino=%s&fecha=%s'%(origen,destino,fecha))
    else:
        form = BuscarViajeForm()
    return render(request,'classroom/buscar/buscar.html',{'form':form})