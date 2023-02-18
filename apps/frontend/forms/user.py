
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

User = get_user_model()

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    privacy = forms.BooleanField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            'first_name',
            'last_name',
            "email",
            "password1",
            "password2"
        )

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        if commit:
            user.save()
        return user

    def clean(self, *args, **kwargs):
        cleaned_data  = super(NewUserForm, self).clean(*args, **kwargs)
        email         = cleaned_data.get('email',         None)

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                _('El email ya está registrado')
            )


    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['privacy'].label = 'Acepto los <a href="{url}" target="_BLANK">{title}</a>'.format(
            url='/legal/terminos-y-condiciones',
            title='Términos y condiciones',
        )

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'image',
        )
    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        if self.instance.dni:
            self.fields['dni'].disabled  = True
            self.fields['dni'].help_text = ''
