from django.contrib import admin

from .models import Client, User, FilesPDF

admin.site.register(Client)
admin.site.register(User)
admin.site.register(FilesPDF)
