from dynamic_preferences.registries import global_preferences_registry

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _

from core.decorators import check_recaptcha
from core.email import UserRegisterEmail, VerificationEmail
from core.tokens import account_activation_token

from ..forms import NewUserForm

global_preferences = global_preferences_registry.manager()

User = get_user_model()


@check_recaptcha
def register(request):
    if request.user.is_authenticated and not request.user.is_guest:
        return redirect('frontend:home')
    next_redirect = request.GET.get('next', None)
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            if not request.user.is_authenticated or not request.user.is_guest:
                user = form.save()
                messages.success(request, _('registro correcto'))
            else:
                new_user = form.save(commit=False)
                user = request.user
                user.is_guest = False
                user.first_name = new_user.first_name
                user.last_name = new_user.last_name
                user.username = new_user.username
                user.email = new_user.email
                user.password = new_user.password
                messages.success(request, _('tu cuenta de invitado ahora ya es una cuenta estandar, bienvenido.'))
                user.save()

            if global_preferences['app__verification_email'] and not user.email_validated:
                VerificationEmail(
                    {'request': request},
                    user
                ).send()
                messages.success(request, _('se ha enviado un mensaje de verificación, debes verificar tu email para recibir notificaciones'))
            else:
                user.is_active = True
                user.save()
                try:
                    UserRegisterEmail(context, user).send()
                except:
                    ...
            login(request, user)

            if next_redirect:
                return redirect(next_redirect)

            return redirect("frontend:home")
        messages.error(request, "Problemas con el registro. Información incorrecta.")
    else:
        form = NewUserForm()

    context = {
        "register_form": form,
        'site_key': settings.RECAPTCHA_PUBLIC_KEY if settings.RECAPTCHA_PUBLIC_KEY else None
    }
    return render(request, 'registration/registration_user.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_validated = True
        user.save()
        messages.success(request, _('Gracias por haber confirmado el email'))
        try:
            UserRegisterEmail(context, user).send()
        except:
            ...
        login(request, user)
        return redirect('frontend:home')
    else:
        messages.error(request, _('Activation link is invalid!'))
        return redirect('frontend:home')


def validate_username(request):
    username = request.POST.get('username', None)
    is_taken = User.objects.filter(username__iexact=username).exists()
    data = {
        'is_taken': is_taken
    }
    if data['is_taken']:
        data['error_message'] = _(f'el usuario {username} ya existe, prueba otro')
    return JsonResponse(data)


def validate_email(request):
    email = request.POST.get('email', None)
    is_taken = User.objects.filter(email__iexact=email).exists()
    data = {
        'is_taken': is_taken
    }
    if data['is_taken']:
        data['error_message'] = _('Ya existe un usuario con este email')
    return JsonResponse(data)


def login_as_guest(request):
    if request.user.is_authenticated:
        messages.error(request, _('ya estas logueado'))
    else:
        last_guest = User.objects.filter(username__startswith='guest_').last()
        if last_guest:
            _, num = last_guest.username.split('_')
        else:
            num = 0
        username = 'guest_{num:05}'.format(num=int(num)+1)
        user = User.objects.create_user(
            username=username,
            is_guest=True,
            password='AntonioCintiaErea'
        )
        if user:
            login(request, user)

    next_redirect = request.GET.get('next', None)
    if next_redirect:
        return redirect(next_redirect)

    return redirect('frontend:home')
