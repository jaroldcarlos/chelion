from django.urls import path
from apps.frontend import views

app_name = 'frontend'

urlpatterns = [
    path('edu.html', views.ViewPage.as_view(), name='edu'),
    path('', views.Home.as_view(), name='home'),
]
