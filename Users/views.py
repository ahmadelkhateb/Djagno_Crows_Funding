from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileRegisterForm, UserRegisterFormUpdate, ProfileUpdate
from django.contrib.auth import login, authenticate
from Projects.models import Project, Category, Rate, Tag, Picture, FeatureProject
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponse


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
            user.is_active = False
            profile_form = ProfileRegisterForm(request.POST, request.FILES, instance=user.profile)
            user.save()
            profile_form.save()

            #######CONFIRMATION##########

            current_site = get_current_site(request)
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your KickPro account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, 'Your account has been created But you have to Activate your account before '
                                      'Trying to login!')
            return redirect('Users:home')
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            # messages.success(request, 'Your account has been created!')
            # return redirect('Users:home')
    else:
        form = UserRegisterForm()
        profile_form = ProfileRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'profile': profile_form})


# Activation Function

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist()):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # profile.save()
        # registered = True
        login(request, user)

        messages.success(request, 'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
        # return redirect('home')
    else:
        messages.success(request, 'Activation link is invalid or Expired!')
        return redirect('login')


@login_required
def profile(request):
    return render(request, 'users/profile.html')


def home(request):
    high_rate_pro = Rate.objects.all().order_by('-rate')[:6]
    images = Picture.objects.none()
    for rate in high_rate_pro:
        images = [x for x in images] + [y for y in rate.project.first_image()]
    latest_pro = FeatureProject.objects.all().order_by('-updated')[:5]
    categories = Category.objects.all()

    context = {'high_rate': high_rate_pro, 'latest_pro': latest_pro, 'cats': categories, 'images': images}
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


@login_required
def edit(request):
    if request.method == 'POST':
        form = UserRegisterFormUpdate(request.POST, instance=request.user)
        profile_form1 = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form1.is_valid():
            form.save()
            profile_form1.save()
            messages.success(request, 'Your account has been updated! ')
            return redirect('profile')

    else:
        form = UserRegisterFormUpdate(instance=request.user)
        profile_form1 = ProfileUpdate(instance=request.user.profile)

    return render(request, 'users/edit.html', {'form': form, 'profile': profile_form1})


@login_required
def delete(request):
    user = request.user
    user.delete()
    return redirect('logout')

