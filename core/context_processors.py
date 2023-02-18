import re

from django import db
from dynamic_preferences.registries import global_preferences_registry
from django.conf import settings
from django.urls import resolve

global_preferences = global_preferences_registry.manager()

def custom_context(request):
    MOBILE_AGENT_RE = re.compile(
        r".*(iphone|mobile|androidtouch)",
        re.IGNORECASE
    )
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        mobile = True
    else:
        mobile = False
    database_name = db.utils.settings.DATABASES['default']['NAME']

    context = {
        'database_name': database_name,
        'mobile': mobile,
        'app_name': global_preferences['app__app_name'],
        'theme_backend': global_preferences['app__app_theme_backend']
    }
    return context
