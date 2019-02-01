from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from Users.models import User
from Projects.models import Project
from Projects.forms import ProjectModelForm


def index(request):
    return HttpResponse("You Did It Sasuke")


def first_form(request,id):
    user_inst = get_object_or_404(User, pk=id)

    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ProjectModelForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            project = form.save(commit=False)
            project.user = user_inst
            project.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Home'))

        # If this is a GET (or any other method) create the default form.
    else:
        form = ProjectModelForm()

    context = {
        'form': form,
        'user_inst': user_inst,
    }

    return render(request, 'first_form.html', context)
