from django.urls import path
from apps.backend.views import activate
from . import views

app_name = "backend"

urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('users/list', views.Users_List.as_view(), name='users_list'),
    path('users/create', views.Users_Create.as_view(), name='users_create'),
    path('users/update/<pk>', views.Users_Update.as_view(), name='users_update'),
    path('users/change-password', views.change_password, name='users_change_password'),
    path('users/delete/<pk>', views.Users_Delete.as_view(), name='users_delete'),

    path('clients/list', views.Clients_List.as_view(), name='clients_list'),
    path('clients/csv', views.clients_to_csv, name='clients_to_csv'),
    path('clients/export', views.client_to_csv_export, name='client_to_csv_export'),
    path('clients/create', views.Clients_Create.as_view(), name='clients_create'),
    path('clients/update/<pk>', views.Clients_Update.as_view(), name='clients_update'),
    path('clients/delete/<pk>', views.Clients_Delete.as_view(), name='clients_delete'),

    path('file/list', views.FilesPDF_List.as_view(), name='file_list'),
]
