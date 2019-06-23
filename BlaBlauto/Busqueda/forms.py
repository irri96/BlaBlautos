from django import forms
from django.forms import widgets


class BuscarViajeForm(forms.Form):
    ciudad_origen = forms.CharField(label='Ciudad de origen')
    ciudad_destino = forms.CharField(label='Ciudad de destino')
    fecha = forms.DateField(widget=widgets.SelectDateWidget)