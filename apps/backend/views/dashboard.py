from django.shortcuts import  render, redirect
from ..forms import RegisterUserForm
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from core.email import UserRegisterEmail, VerificationEmail
from core.tokens import account_activation_token
from django.utils.translation import gettext as _
from dynamic_preferences.registries import global_preferences_registry
from core.decorators import check_recaptcha


User=get_user_model()

global_preferences = global_preferences_registry.manager()
theme_backend = global_preferences['app__app_theme_backend']

class home(TemplateView):
    template_name = f'backend/{theme_backend}/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@check_recaptcha
def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid() and request.recaptcha_is_valid:
            user = form.save()
            context = {
                'request':request
            }
            if global_preferences['app__verification_email']:
                VerificationEmail(context, user).send()
                messages.success(request, _('verification email has been sent'))
            else:
                UserRegisterEmail(context, user).send()
            login(request, user)
            messages.success(request, _('registration successful'))
            return redirect("frontend:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = RegisterUserForm()
    context = {
        "register_form":form,
        'site_key': settings.RECAPTCHA_PUBLIC_KEY if settings.RECAPTCHA_PUBLIC_KEY else None
    }
    return render (request, 'registration/registration_user.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, _('Thank you for your email confirmation'))
        login(request, user)
        return redirect('frontend:home')
    else:
        messages.error(request, _('Activation link is invalid!'))
        return redirect('frontend:home')
