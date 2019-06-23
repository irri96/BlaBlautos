from django.urls import path,include
from .views import ChoferSignUpView,PasajeroSignUpView,ver_perfil
urlpatterns = [
    path('accounts/signup/pasajero', PasajeroSignUpView.as_view(), name='pasajero_signup'),
    path('accounts/signup/chofer', ChoferSignUpView.as_view(), name='chofer_signup'),
    path(r'perfil/<int:id>/', ver_perfil, name="ver_perfil")
]
