from django.urls import path
from apps.frontend import views

app_name = 'frontend'

urlpatterns = [
    path('<str:name>.html', views.viewpage, name='nombre'),
    path('', views.Home.as_view(), name='home'),
]
