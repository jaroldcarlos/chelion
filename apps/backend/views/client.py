from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
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

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(agent=self.request.user)
        return queryset

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class Clients_Create(CreateView):
    model = Client
    template_name = f'backend/{theme_backend}/clients/create.html'
    fields = '__all__'

    def get_initial(self):
        initial = super(Clients_Create, self).get_initial()
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            initial['agent'] = self.request.user
        return initial

    def form_valid(self, form):
        name_business = form.cleaned_data['name']
        messages.success(self.request, f'you have successfully created the client: {name_business}')
        return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
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

    def test_func(self):
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            obj = self.get_object()
            return obj.agent == self.request.user
        else:
            return True

    def form_valid(self, form):
        name_business = form.cleaned_data['name']
        messages.success(self.request, f'you have successfully updated the client: {name_business}')
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('continue_editing'):
            return reverse_lazy('backend:clients_update', args=[self.object.pk])
        else:
            return reverse('backend:clients_list')
