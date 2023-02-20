from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from apps.backend.views import register

from dynamic_preferences.registries import global_preferences_registry

global_preferences = global_preferences_registry.manager()

admin_title = global_preferences['app__app_name']
admin.site.site_header = admin_title
admin.site.index_title = admin_title
admin.site.site_title = admin_title

handler500 = 'apps.frontend.views.custom_error_view'
handler404 = 'apps.frontend.views.custom_page_not_found_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/', include('apps.backend.urls')),
    path('register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('apps.frontend.urls'))
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [path('rosetta/', include('rosetta.urls'))]

if 'dynamic_preferences' in settings.INSTALLED_APPS:
    urlpatterns = [
        path('preferences/', include('dynamic_preferences.urls'))
    ] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
