from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from Nucleo.models import Pasajero,Chofer,User



class PasajeroSignUpForm(UserCreationForm):
    rut = forms.IntegerField()
    nacimiento = forms.DateField(widget=forms.SelectDateWidget(years=range(1900,2019)))
    celular = forms.IntegerField()
    fumador = forms.BooleanField(required=False,widget=forms.CheckboxInput)
    mascotas = forms.BooleanField(required=False)
    musica = forms.BooleanField(required=False)
    descripcion = forms.CharField(required=False)
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.es_pasajero = True
        user.nacimiento=self.cleaned_data.get('nacimiento')
        user.celular = self.cleaned_data.get('celular')
        user.fumador= self.cleaned_data.get('fumador')
        user.mascotas = self.cleaned_data.get('mascotas')
        user.musica = self.cleaned_data.get('musica')
        user.descripcion = self.cleaned_data.get('descripcion')

        user.save()
        pasajero = Pasajero.objects.create(user=user)
        return user



class ChoferSignUpForm(UserCreationForm):
    rut = forms.IntegerField()
    nacimiento = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2019)))
    celular = forms.IntegerField()
    fumador = forms.BooleanField(required=False)
    mascotas = forms.BooleanField(required=False)
    musica = forms.BooleanField(required=False)
    descripcion = forms.CharField(required=False)

    licencia = forms.CharField(required=True)
    clase = forms.CharField(required=True)
    patente = forms.CharField(required=True)
    marca = forms.CharField(required=True)
    año = forms.CharField(required=True)
    color = forms.CharField(required=True)
    asientos = forms.IntegerField(min_value=1,max_value=6,required=True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.es_chofer = True
        user.nacimiento = self.cleaned_data.get('nacimiento')
        user.celular = self.cleaned_data.get('celular')
        user.fumador = self.cleaned_data.get('fumador')
        user.mascotas = self.cleaned_data.get('mascotas')
        user.musica = self.cleaned_data.get('musica')
        user.descripcion = self.cleaned_data.get('descripcion')

        user.save()
        self.cleaned_data.get('licencia')
        chofer = Chofer.objects.create(user=user,
                                       licencia=self.cleaned_data.get('licencia'),
                                       clase=self.cleaned_data.get('clase'),
                                       patente=self.cleaned_data.get('patente'),
                                       marca=self.cleaned_data.get('marca'),
                                       año=self.cleaned_data.get('año'),
                                       color=self.cleaned_data.get('color'),
                                       asientos=self.cleaned_data.get('asientos'))
        return user
