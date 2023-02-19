from django import template

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.backend.models import Client, Province

register = template.Library()

User = get_user_model()

@register.inclusion_tag('templatetags/bart.html')
def bart_users():
    data = []
    users = User.objects.filter(is_staff=False, is_superuser=False)
    clients = Client.objects.all()

    if users:
        for user in users:
            users_clients = clients.filter(agent=user.pk).count()
            data.append([f"{ user.username }", users_clients ])

    context = {
        'id': 'bart_users',
        'title': _('data by users'),
        'data':data
    }
    return context


@register.inclusion_tag('templatetags/bart.html')
def bart_companies():
    data = []
    clients = Client.objects.all()
    company_chelion = clients.filter(business=1).count()
    data.append(['Chelion Iberia', company_chelion ])
    company_iberian = clients.filter(business=2).count()
    data.append(['Iberian Trade Europe', company_iberian ])
    context = {
        'id': 'bart_companies',
        'title': _('data by companies'),
        'data':data
    }
    return context


@register.inclusion_tag('templatetags/bart.html')
def bart_clients():
    data = []
    clients = Client.objects.all()
    new_clients = clients.filter(new_client=True).count()
    data.append(['New Clients', new_clients ])
    old_clients = clients.filter(new_client=False).count()
    data.append(['Old Client', old_clients ])
    context = {
        'id': 'bart_clients',
        'title': _('data by clients'),
        'data':data
    }
    return context


@register.inclusion_tag('templatetags/map.html')
def map():
    provinces = Province.objects.all()

    context = {
        'provinces':provinces
    }
    return context
