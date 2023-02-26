from django.shortcuts import render
from django.views.generic.base import RedirectView, TemplateView


class Home(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'backend:home'

def viewpage(request, name=None):
    template_name = "view.html"
    context = {
        'name':name
    }
    return render(request, template_name, context)

def custom_page_not_found_view(request, exception=None):
    return render (request, '404.html', {})

def custom_error_view(request, exception=None):
    return render(request, "500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "errors/403.html", {})

def custom_bad_request_view(request, exception=None):
    return render(request, "errors/400.html", {})

