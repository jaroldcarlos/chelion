from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser




class User(AbstractUser):
    image = models.ImageField(_('image'), blank=True, null=True)
    validated_email = models.BooleanField(_('validated email'), default=False)

    def get_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return f'{ self.username }'


def get_agent_choice():
    list_user = [
        ("1", "None")
    ]
    users = User.objects.filter(is_superuser=False, is_staff=False)
    if users:
        for user in users:
            list_user.append((f'{user.pk}', f'{user.get_name()}'))
    return list_user

class Client(models.Model):
    BUSINESS_CHOICES = (
        ("1", "Chelion Iberia"),
        ("2", "Iberian Trade Europe"),
        ("3", "Ambos"),
    )

    AGENT_CHOICES = (
        ("1", "Mario"),
        ("2", "Pablo"),
        ("3", "Miguel Angel"),
    )
    INTEREST_CHOICES = (
        ("1", "Blue"),
        ("2", "Yellow"),
        ("3", "Red"),
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    business = models.CharField(_('business'), max_length=10, choices = BUSINESS_CHOICES, default="1")
    agent = models.CharField(_('agent'), max_length=10, choices = get_agent_choice(), default="1")
    name = models.CharField(_('company name'), max_length=200)
    address = models.CharField(_('address'), blank=True, null=True, max_length=200)
    zipcode = models.CharField(_('postal code'), blank=True, null=True, max_length=200)
    web = models.CharField(_('web'),blank=True, null=True, max_length=200)
    cif = models.CharField(_('CIF'), max_length=20, blank=True, null=True)
    contact_person = models.CharField(_('contact person'), max_length=200)
    person_position = models.CharField(_('persons position'), max_length=200)
    email = models.EmailField(_('email'))
    telephone = models.CharField(_('telephone'), max_length=20, blank=True, null=True)

    #NEW_USER
    new_client =  models.BooleanField(_('new client'), default=False, help_text='if check is a new client')

    #ACTIVITY
    a_installer =  models.BooleanField(_('installer'), default=False)
    a_distributor = models.BooleanField(_('distributor'), default=False)
    a_meter =   models.BooleanField(_('EPC'), default=False)
    a_engineering =   models.BooleanField(_('engineering'), default=False)

    #Interest
    i_storage =  models.BooleanField(_('storage'), default=False)
    i_investor =  models.BooleanField(_('inverter'), default=False)
    i_charger =  models.BooleanField(_('charger'), default=False)
    i_panels =  models.BooleanField(_('panels'), default=False)
    i_others =  models.BooleanField(_('others'), default=False)
    #i_comment = models.TextField(_('note'), blank=True, null=True)

    #Traffic Light of Interest
    interest = models.CharField(_('interest'), max_length=1, choices = INTEREST_CHOICES, default="1")

    comment = models.TextField(_('comment'), blank=True, null=True)


    def __str__(self):
        return f'{self.name}'


class FilesPDF(models.Model):
    name = models.CharField(_('name'), max_length=200)
    file = models.FileField(_('file'),upload_to ='file/', blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

