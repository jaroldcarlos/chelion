from django import template

from datetime import datetime
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from apps.backend.models import Client, Province

register = template.Library()

User = get_user_model()

@register.inclusion_tag('templatetags/bart.html')
def bart_users():
    data = []
    users = User.objects.filter(is_staff=False, is_superuser=False).annotate(num_clients = Count('clients')).order_by('-num_clients').exclude(num_clients__lte=0)
    clients = Client.objects.all()

    if users:
        for user in users:
            data.append([f"{ user.get_name.title() }", user.clients.all().count()])

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
    company = clients.filter(business=3).count()
    company_chelion = clients.filter(business=1).count()
    data.append(['Chelion Iberia', company_chelion + company])
    company_iberian = clients.filter(business=2).count()
    data.append(['Iberian Trade Europe', company_iberian + company])
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
        'title': _('data clients'),
        'data':data
    }
    return context

@register.inclusion_tag('templatetags/statistics.html')
def statistics():
    clients = Client.objects.all()
    new_clients_total = clients.filter(new_client=True).count()
    users = User.objects.filter(is_staff=False, is_superuser=False).annotate(num_clients = Count('clients')).order_by('-num_clients').exclude(num_clients__lte=0)[0:3]
    context = {
        'new_clients_total':new_clients_total,
        'users':users
    }
    return context

@register.inclusion_tag('templatetags/line-chart.html')
def line_chart():

    data = []
    clients = Client.objects.all()

    fecha1 = datetime.strptime("2023-02-19", "%Y-%m-%d")
    fecha1_count = clients.filter(Q(business=1) | Q(business=3) , created_on__date=fecha1).count()

    fecha2 = datetime.strptime("2023-02-20", "%Y-%m-%d")
    fecha2_count = clients.filter(Q(business=1) | Q(business=3) , created_on__date=fecha2).count()

    fecha3 = datetime.strptime("2023-02-21", "%Y-%m-%d")
    fecha3_count = clients.filter(Q(business=1) | Q(business=3) , created_on__date=fecha3).count()

    fecha4 = datetime.strptime("2023-02-22", "%Y-%m-%d")
    fecha4_count = clients.filter(Q(business=1) | Q(business=3) , created_on__date=fecha4).count()

    fecha5 = datetime.strptime("2023-02-23", "%Y-%m-%d")
    fecha5_count = clients.filter(Q(business=1) | Q(business=3) , created_on__date=fecha5).count()

    data.append(['Chelion Iberia', f'{fecha1_count}, {fecha2_count}, {fecha3_count}, {fecha4_count}, {fecha5_count}', 'red'])

    fecha1 = datetime.strptime("2023-02-19", "%Y-%m-%d")
    fecha1_count = clients.filter(Q(business=2) | Q(business=3), created_on__date=fecha1).count()

    fecha2 = datetime.strptime("2023-02-20", "%Y-%m-%d")
    fecha2_count = clients.filter(Q(business=2) | Q(business=3), created_on__date=fecha2).count()

    fecha3 = datetime.strptime("2023-02-21", "%Y-%m-%d")
    fecha3_count = clients.filter(Q(business=2) | Q(business=3), created_on__date=fecha3).count()

    fecha4 = datetime.strptime("2023-02-22", "%Y-%m-%d")
    fecha4_count = clients.filter(Q(business=2) | Q(business=3), created_on__date=fecha4).count()

    fecha5 = datetime.strptime("2023-02-23", "%Y-%m-%d")
    fecha5_count = clients.filter(Q(business=2) | Q(business=3), created_on__date=fecha5).count()

    data.append(['Iberian Trade Europe', f'{fecha1_count}, {fecha2_count}, {fecha3_count}, {fecha4_count}, {fecha5_count}', 'blue'])

    context = {
        'title': _('clients per day (Business)'),
        'data': data
    }

    return context

@register.inclusion_tag('templatetags/map.html')
def map():
    provinces = Province.objects.all().annotate(num_clients = Count('clients')).order_by('-num_clients').exclude(num_clients__lte=0)
    clients = Client.objects.all().count()
    context = {
        'clients_total': clients,
        'provinces':provinces,
        'title': _('map of clients by provinces'),
    }
    return context


