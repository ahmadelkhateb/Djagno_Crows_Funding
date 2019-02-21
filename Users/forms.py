from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.forms import ModelForm, TextInput, ValidationError


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count() > 0:
            raise ValidationError(u'This email address is already registered.')
        return email


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

