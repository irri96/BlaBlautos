from Nucleo.models import Viaje
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

class CrearForm(forms.ModelForm):
    tiempo_final = forms.DateTimeField()
    class Meta:
        model = Viaje
        fields = ( 'ciudad_origen', 'ciudad_destino', 'asientos','tiempo_inicio')