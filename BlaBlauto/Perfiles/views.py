from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from Nucleo.models import *
from .forms import *

class ChoferSignUpView(CreateView):
    model = User
    form_class = ChoferSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'chofer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class PasajeroSignUpView(CreateView):
    model = User
    form_class = PasajeroSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'pasajero'
        return super().get_context_data(**kwargs)
    #aaaaaaaaaaaaa
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

def ver_perfil(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return redirect("/")
    if user.es_chofer:
        try:
            chofer = Chofer.objects.get(user=User(id=user.id))
            return render(request, "perfil.html",{"usuario":user,"chofer":chofer})
        except:
            pass
    return render(request, "perfil.html",{"usuario":user})