from html2text import HTML2Text

from django.conf import settings
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.utils.encoding import force_bytes
from dynamic_preferences.registries import global_preferences_registry
from django.contrib.sites.shortcuts import get_current_site
from render_block import render_block_to_string

from core.tokens import account_activation_token


global_preferences = global_preferences_registry.manager()


class Email:
    template = "email/base.html"
    from_email = settings.DEFAULT_FROM_EMAIL

    def __init__(self, context, to_email=None):
        self.to_email = to_email
        self.subject = render_block_to_string(self.template, 'subject', context)
        self.plain = render_block_to_string(self.template, 'plain', context)
        self.html = render_block_to_string(self.template, 'html', context)
        # self.domain = get_current_site(context['request']).get_host

        if self.plain == "":
            h = HTML2Text()
            h.ignore_images = True
            h.ignore_emphasis = True
            h.ignore_tables = True
            self.plain = h.handle(self.html)

    def send(self):
        send = send_mail(
            self.subject,
            self.plain,
            self.from_email,
            [self.to_email],
            html_message=self.html,
            fail_silently=False
        )
        if send:
            return True
        else:
            return False


class UserEmail(Email):
    def __init__(self, context, user):
        self.user = user
        self.domain = get_current_site(context['request']).domain

        context = {
            'user': self.user,
            'domain': self.domain,
            **context
        }

        super().__init__(context)
        self.to_email = self.user.email


class VerificationEmail(Email):
    template = "email/verification.html"

    def __init__(self, context, user):
        self.user = user
        context = {
            'user': self.user,
            'domain': self.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token': account_activation_token.make_token(self.user),
            **context
        }
        super().__init__(context)
        self.to_email = self.user.email


class UserRegisterEmail(UserEmail):
    template = "email/register.html"


class SendCodeEmail(Email):
    template = "email/sendcode.html"

class SendCodeGiftEmail(Email):
    template = "email/sendcode_gift.html"
