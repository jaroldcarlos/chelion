from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from dynamic_preferences.registries import global_preferences_registry
from ..models import Client

global_preferences = global_preferences_registry.manager()
theme_backend = global_preferences['app__app_theme_backend']


class Clients_List(ListView):
    queryset = Client.objects.all()
    template_name = f'backend/{theme_backend}/clients/list.html'
    context_object_name = 'clients'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class Clients_Create(CreateView):
    model = Client
    template_name = f'backend/{theme_backend}/clients/create.html'
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('backend:clients_list')


class Clients_Delete(DeleteView):
    model=Client
    template_name=f'backend/{theme_backend}/clients/delete.html'
    success_url=reverse_lazy("backend:clients_list")

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Clients_Update(UpdateView):
    model = Client
    template_name = f'backend/{theme_backend}/clients/update.html'
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('backend:clients_list')
