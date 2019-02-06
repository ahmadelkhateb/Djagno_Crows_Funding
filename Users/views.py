from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileRegisterForm
from django.contrib.auth import login, authenticate


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profile_form = ProfileRegisterForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.refresh_from_db()
            profile_form = ProfileRegisterForm(request.POST, request.FILES, instance=user.profile)
            profile_form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('Users:home')
    else:
        form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'profile': profile_form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def home(request):
    return render(request, 'users/home.html')

@login_required
def about(request):
    return render(request, 'users/about.html', {'title': 'About'})
