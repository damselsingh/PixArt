from django import forms
from .models import People
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, UserChangeForm
from django.contrib.auth.models import User

class feeds(forms.ModelForm):
    class Meta:
        model = People
        fields = ['image', 'caption']
        widgets = {'caption': forms.Textarea, 'image': forms.FileInput(attrs = {'class': 'img-form'})}
        labels = {'image': 'Upload here', 'caption': 'Caption for the picture'}
   
    

class SignUpForm(UserCreationForm):
    password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs = {'class': 'form-control'}))
    password2=forms.CharField(label="Confirm Password(again)", widget=forms.PasswordInput(attrs = {'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email', 'first_name': 'First Name', 'last_name': 'Last Name'}
        widgets = {'username': forms.TextInput(attrs = {'class': 'form-control'}),
        'first_name': forms.TextInput(attrs = {'class': 'form-control'}),
        'last_name': forms.TextInput(attrs = {'class': 'form-control'}),
        'email': forms.EmailInput(attrs = {'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
   username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
   password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
   'class': 'form-control'}))

class EditUserChangeForm(UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'last_login']
        labels = {'email': 'Email'}