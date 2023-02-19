from django import template

from django.contrib.auth import get_user_model
from apps.backend.models import Client

register = template.Library()

User = get_user_model()

@register.inclusion_tag('templatetags/bart_users.html')
def bart_users():
    data = []
    users = User.objects.filter(is_staff=False, is_superuser=False)
    clients = Client.objects.all()

    if users:
        for user in users:
            users_clients = clients.filter(agent=user.pk).count()
            data.append([f"{ user.username }", users_clients ])

    context = {
        'data':data
    }
    return context
