from django.urls import path,include
from .views import ChoferSignUpView,PasajeroSignUpView
urlpatterns = [
    path('accounts/signup/pasajero', PasajeroSignUpView.as_view(), name='pasajero_signup'),
    path('accounts/signup/chofer', ChoferSignUpView.as_view(), name='chofer_signup')
]
