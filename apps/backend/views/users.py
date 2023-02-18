
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from dynamic_preferences.registries import global_preferences_registry

User=get_user_model()
global_preferences = global_preferences_registry.manager()
theme_backend = global_preferences['app__app_theme_backend']

class Users_List(ListView):
    queryset = User.objects.filter(is_superuser=False)
    template_name = f'backend/{theme_backend}/users/list.html'
    context_object_name = 'users'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class Users_Create(CreateView):
    model = User
    template_name = f'backend/{theme_backend}/users/create.html'
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "password"
    ]

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('backend:users_list')


class Users_Delete(DeleteView):
    model=User
    template_name=f'backend/{theme_backend}/users/delete.html'
    success_url=reverse_lazy("backend:users_list")

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Users_Update(UpdateView):
    model = User
    template_name = f'backend/{theme_backend}/users/update.html'
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
    ]

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('backend:users_list')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('change_password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, f'backend/{theme_backend}/users/change_password.html', {
        'form': form
    })

