from django.views.generic import ListView, CreateView, DeleteView, UpdateView

from dynamic_preferences.registries import global_preferences_registry

from ..models import FilesPDF

global_preferences = global_preferences_registry.manager()
theme_backend = global_preferences['app__app_theme_backend']


class FilesPDF_List(ListView):
    queryset = FilesPDF.objects.all()
    template_name = f'backend/{theme_backend}/files/list.html'
    context_object_name = 'files'

