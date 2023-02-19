from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Client

User = get_user_model()

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_staff', 'username', 'first_name','last_name', 'email', 'password']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
