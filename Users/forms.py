from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms import ModelForm, TextInput


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class ProfileRegisterForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'image']


class ProfileUpdate(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'birth_date','facebook_profile','country','image']
        widgets = {
            'birth_date': TextInput(attrs={'type': 'date'}),
        }


class UserRegisterFormUpdate(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

