import csv
import copy

from django.utils import timezone
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from ..models import Client
from ..forms import ClientForm

if 'dynamic_preferences' in settings.INSTALLED_APPS:
    from dynamic_preferences.registries import global_preferences_registry
    global_preferences = global_preferences_registry.manager()
    theme_backend = global_preferences['app__app_theme_backend']
else:
    theme_backend = 'default'

class Clients_List(ListView):
    queryset = Client.objects.all()
    template_name = f'backend/{theme_backend}/clients/list.html'
    context_object_name = 'clients'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            queryset = queryset.filter(agent=self.request.user)
        return queryset

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class Clients_Create(CreateView):
    model = Client
    form_class  = ClientForm
    template_name = f'backend/{theme_backend}/clients/create.html'

    def get_initial(self):
        initial = super(Clients_Create, self).get_initial()
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            initial['agent'] = self.request.user
        initial['created_on'] = timezone.now().date()
        return initial

    def form_valid(self, form):
        name_business = form.cleaned_data['name']
        messages.success(self.request, f'you have successfully created the client: {name_business}')
        return super().form_valid(form)

    @method_decorator(user_passes_test(lambda u: u.is_authenticated))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('backend:clients_list')


class Clients_Delete(DeleteView):
    model=Client
    template_name=f'backend/{theme_backend}/clients/delete.html'
    success_url=reverse_lazy("backend:clients_list")

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Clients_Update(UpdateView):
    model = Client
    form_class  = ClientForm
    template_name = f'backend/{theme_backend}/clients/update.html'

    def test_func(self):
        if not self.request.user.is_staff and not self.request.user.is_superuser:
            obj = self.get_object()
            return obj.agent == self.request.user
        else:
            return True

    def form_valid(self, form):
        name_business = form.cleaned_data['name']
        messages.success(self.request, f'you have successfully updated the client: {name_business}')
        return super().form_valid(form)

    def get_success_url(self):
        if self.request.GET.get('continue_editing'):
            return reverse_lazy('backend:clients_update', args=[self.object.pk])
        else:
            return reverse('backend:clients_list')

@user_passes_test(lambda u: u.is_staff)
def clients_to_csv(request):
    queryset = Client.objects.all()
    filename = "clients.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)

    fields = Client.get_fields()

    writer.writerow(fields)

    for obj in queryset:
        row = [getattr(obj, field) for field in fields]
        writer.writerow(row)

    return response


@user_passes_test(lambda u: u.is_staff)
def client_to_csv_export(request):
    queryset = Client.objects.all()
    filename = "export_new_clients.csv"
    client_list = []
    BASE_CLIENT = {
        'POSALIAS':'',
        'CODPOS':'',
        'PROVIFISCAL':'',
        'RUTA':'',
        'ZONA':'',
        'CODMUNICIPIO':'',
        'CODMUNICIPIOFISCAL':'',
        'CODPAIS':'',
        'DTOPOS':'',
        'DTOFISCAL':'',
        'CODPROVI':'',
        'CODREP':'',
        'COMENTARIO':'',
        'DIRPOS':'',
        'DIRPOS1':'',
        'DIRPOS2':'',
        'DIRFISCAL':'',
        'E_MAIL':'',
        'EMAILFISCAL':'',
        'E_MAIL_PUBLI':'',
        'ENVIARDOC':'',
        'ESCALERA':'',
        'ESCALERAFISCAL':'',
        'EXTENSIONFISCAL':'',
        'FAXPOS':'',
        'FAXFISCAL':'',
        'FECALTA_ORG':'',
        'FECALTA':'',
        'AP_ID':'',
        'IDORG':'',
        'LINKEDIN':'',
        'SKYPE':'',
        'TWITTER':'',
        'MODIFICADO':'',
        'MOTIVOBLOQUEO':'',
        'MOTIVOBLOQUEO_ORG':'',
        'MUNICIPIO':'',
        'MUNICIPIOFISCAL':'',
        'NIFPOS':'',
        'ORDENRUTA':'',
        'NVIA':'',
        'RAZON':'',
        'NVIAFISCAL':'',
        'OBSERVACIONES':'',
        'OBSPOS':'',
        'OBSOLETO':'',
        'NOMPOS':'',
        'PAGINAWEB':'',
        'PAISFISCAL':'',
        'PISO':'',
        'PISOFISCAL':'',
        'POBPOS':'',
        'POBFISCAL':'',
        'PUERTA':'',
        'PUERTAFISCAL':'',
        'NOMFISCAL':'',
        'REFERENCIA':'',
        'TELPOS':'',
        'TELPOS2':'',
        'TELEFONOFISCAL':'',
        'TELEFONO2FISCAL':'',
        'TIPODOCNIF':'',
        'TIPOIMAGEN':'',
        'TIPONUMERO':'',
        'TIPONUMEROFISCAL':'',
        'ULTFECMOD':'',
        'VIA':'',
        'VIAFISCAL':'',
        'VIAPUBLICAFISCAL':''
    }
    for client in queryset:
        new_client = copy.deepcopy(BASE_CLIENT)
        new_client['FECALTA_ORG'] = client.created_on.strftime("%d/%m/%Y")
        new_client['FECALTA'] = client.created_on.strftime("%d/%m/%Y")
        if client.name:
            new_client['POSALIAS'] = client.name
            new_client['RAZON'] = client.name
            new_client['NOMPOS'] = client.name
        if client.province:
            new_client['POBPOS'] = 'ES'
            new_client['POBPOS'] = client.province.name
        if client.zipcode:
            new_client['DTOPOS'] = client.zipcode
            new_client['DTOFISCAL'] = client.zipcode
        if client.email:
            new_client['E_MAIL'] = client.email
        if client.comment:
            new_client['OBSERVACIONES'] = client.comment
        if client.web:
            new_client['PAGINAWEB'] = client.web
        if client.telephone:
            new_client['TELPOS2'] = client.telephone
        if client.address:
            new_client['VIAFISCAL'] = client.address
            new_client['DIRPOS'] = client.address
        client_list.append(new_client)



    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    writer = csv.DictWriter(
        response,
        fieldnames=BASE_CLIENT.keys(),
        delimiter=';',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )
    writer.writeheader()
    for row in client_list:
        writer.writerow(row)

    return response

