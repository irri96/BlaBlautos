from django.urls import include, path

from Nucleo.views import Inicio

urlpatterns = [
    path('', include('Nucleo.urls')),
    path('', include('Perfiles.urls')),
    path('', include('Busqueda.urls')),
    path('', include('AdministracionReservas.urls')),
    path('', include('AdministracionViajes.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', Inicio.SignUpView.as_view(), name='signup')
]
