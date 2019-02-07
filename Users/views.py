from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileRegisterForm
from django.contrib.auth import login, authenticate
from Projects.models import Project, Category, Rate, Tag
from django.core.exceptions import ObjectDoesNotExist


def register(request):
    if request.user.is_authenticated:
        messages.success(request, 'You are Already signed with account')
        return redirect('Users:home')

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
            messages.success(request, 'Your account has been created!')
            return redirect('Users:home')
    else:
        form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'profile': profile_form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def home(request):
    high_rate_pro = Rate.objects.all().order_by('-rate')[:6]
    latest_pro = Project.objects.all().order_by('-pub_date')[:5]
    categories = Category.objects.all()

    context = {'high_rate': high_rate_pro, 'latest_pro': latest_pro, 'cats': categories}
    return render(request, 'users/home.html', context)

@login_required
def search(request):
    search_key = request.GET.get('search', False)
    if search_key:
        search_key = request.GET['search']
        try:
            tag = Tag.objects.get(tag=search_key)
        except ObjectDoesNotExist:
            projects = Project.objects.none()
        else:
            projects = tag.project_set.all()

        title_pro = Project.objects.filter(title=search_key)
        records = (projects | title_pro).distinct()
        if not records:
            message = "Couldn't Find Any matching Project"
        else:
            message = "Search Results"
        context = {'message': message, 'records': records}
        return render(request, 'users/search.html', context)
    else:
        return redirect('Users:home')
