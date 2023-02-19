from django.contrib import admin

from .models import Client, User, FilesPDF, Province

admin.site.register(Client)
admin.site.register(User)
admin.site.register(Province)
admin.site.register(FilesPDF)
