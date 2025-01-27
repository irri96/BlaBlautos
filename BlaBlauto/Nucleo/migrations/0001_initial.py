# Generated by Django 2.0.1 on 2019-06-23 18:48

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('realizado', models.BooleanField(default=False)),
                ('asientos', models.IntegerField()),
                ('estado_pago', models.BooleanField()),
                ('estado_reserva', models.PositiveSmallIntegerField(choices=[(1, 'EN_ESPERA'), (2, 'ACEPTADO'), (3, 'RECHAZADO')], default=1)),
            ],
            options={
                'verbose_name': 'Reservación',
                'verbose_name_plural': 'Reservaciones',
            },
        ),
        migrations.CreateModel(
            name='Tramo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_final', models.TimeField()),
                ('precio', models.IntegerField()),
                ('asientos_libres', models.IntegerField()),
                ('ciudad_origen', models.CharField(max_length=30)),
                ('ciudad_destino', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valoracion', models.IntegerField()),
                ('comentario', models.CharField(max_length=140)),
            ],
            options={
                'verbose_name': 'Valoración',
                'verbose_name_plural': 'Valoraciones',
            },
        ),
        migrations.CreateModel(
            name='Viaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiempo_inicio', models.DateTimeField()),
                ('asientos', models.IntegerField()),
                ('ciudad_origen', models.CharField(max_length=30)),
                ('ciudad_destino', models.CharField(max_length=30)),
                ('en_curso', models.BooleanField(default=False)),
                ('realizado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('es_chofer', models.BooleanField(default=False)),
                ('es_pasajero', models.BooleanField(default=False)),
                ('rut', models.IntegerField(default=0)),
                ('nacimiento', models.DateField(default=django.utils.timezone.now)),
                ('celular', models.BigIntegerField(default=0)),
                ('fumador', models.BooleanField(default=False)),
                ('mascotas', models.BooleanField(default=False)),
                ('musica', models.BooleanField(default=False)),
                ('descripcion', models.CharField(default='', max_length=140)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Chofer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('licencia', models.CharField(max_length=10)),
                ('clase', models.CharField(max_length=10)),
                ('patente', models.CharField(max_length=10)),
                ('marca', models.CharField(max_length=20)),
                ('modelo', models.CharField(max_length=20)),
                ('año', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=20)),
                ('asientos', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Chofer',
                'verbose_name_plural': 'Choferes',
            },
        ),
        migrations.CreateModel(
            name='Pasajero',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='valoracion',
            name='emisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emisor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='valoracion',
            name='receptor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tramo',
            name='viaje',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tramos', to='Nucleo.Viaje'),
        ),
        migrations.AddField(
            model_name='reservacion',
            name='tramos',
            field=models.ManyToManyField(related_name='reservas_del_tramo', to='Nucleo.Tramo'),
        ),
        migrations.AddField(
            model_name='viaje',
            name='conductor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Nucleo.Chofer'),
        ),
        migrations.AddField(
            model_name='reservacion',
            name='pasajero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Nucleo.Pasajero'),
        ),
    ]
