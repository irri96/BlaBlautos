from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
import django.utils.timezone
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class User(AbstractUser):
    es_chofer = models.fields.BooleanField(default=False,)
    es_pasajero = models.fields.BooleanField(default=False)
    rut = models.fields.IntegerField(default=0)
    nacimiento = models.fields.DateField(default=django.utils.timezone.now)
    celular = models.fields.BigIntegerField(default=0)
    fumador = models.fields.BooleanField(default=False)
    mascotas = models.fields.BooleanField(default=False)
    musica = models.fields.BooleanField(default=False)
    descripcion = models.fields.CharField(max_length=140,default="")
    def __str__(self):
        return self.email

class Pasajero(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    def __str__(self):
        return self.user.username

class Chofer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    licencia = models.CharField(max_length=10)
    clase = models.CharField(max_length=10)
    patente = models.CharField(max_length=10)
    marca = models.CharField(max_length=20)
    modelo = models.CharField(max_length=20)
    año = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    asientos = models.IntegerField()
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = "Chofer"
        verbose_name_plural = "Choferes"

class Valoracion(models.Model):
    valoracion = models.fields.IntegerField()
    comentario = models.fields.CharField(max_length=140)
    emisor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='emisor')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE,related_name='receptor')
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = "Valoración"
        verbose_name_plural = "Valoraciones"

class Viaje(models.Model):
    conductor = models.ForeignKey(Chofer,on_delete=models.CASCADE)
    tiempo_inicio = models.fields.DateTimeField()
    asientos = models.fields.IntegerField()
    ciudad_origen = models.fields.CharField(max_length=30)
    ciudad_destino = models.fields.CharField(max_length=30)
    en_curso = models.fields.BooleanField(default=False)
    realizado = models.fields.BooleanField()
    def __str__(self):
        return str(self.id)
    def limpiar_reservas(self):
        print("TAN BORRANDO A UN WEON")
        for tramo in self.tramos.all():
            for reserva in tramo.reservas_del_tramo.all():
                reserva.delete()

class Tramo(models.Model):
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE,related_name='tramos')
    hora_inicio = models.fields.TimeField()
    hora_final = models.fields.TimeField()
    precio = models.fields.IntegerField()
    asientos_libres = models.fields.IntegerField()
    ciudad_origen = models.fields.CharField(max_length=30)
    ciudad_destino = models.fields.CharField(max_length=30)
    def __str__(self):
        return str(self.id)

class Reservacion(models.Model):
    tramos = models.ManyToManyField(Tramo,related_name='reservas_del_tramo')
    realizado = models.fields.BooleanField(default=False) # True si el pasajero efectivamente realizó el viaje (se subio)
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    asientos = models.fields.IntegerField()
    estado_pago = models.fields.BooleanField()
    EN_ESPERA=1
    ACEPTADO=2
    RECHAZADO=3
    ESTADOS_POSIBLES=(
        (1,'EN_ESPERA'),
        (2,'ACEPTADO'),
        (3,'RECHAZADO')
    )
    estado_reserva = models.PositiveSmallIntegerField(choices=ESTADOS_POSIBLES,default=EN_ESPERA)
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = "Reservación"
        verbose_name_plural = "Reservaciones"

