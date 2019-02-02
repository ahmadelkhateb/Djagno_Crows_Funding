from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from Users.models import User
from Projects.models import Project, Picture, Tag
from Projects.forms import ProjectModelForm, CommentModelForm
from django.forms import modelformset_factory
from django.db.models import Avg


def index(request):
    return HttpResponse("You Did It Sasuke")


def first_form(request, id):
    user_inst = get_object_or_404(User, pk=id)
    PicFormset = modelformset_factory(Picture, fields=('image',), extra=4)
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ProjectModelForm(request.POST)
        formset = PicFormset(request.POST,request.FILES)
        # Check if the form is valid:
        if form.is_valid() and formset.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            project = form.save(commit=False)
            project.user = user_inst
            project.save()
            tags_str = request.POST['tag'].split(',')
            for tag in tags_str:
                tag = Tag(tag=tag)
                tag.save()
                project.tags.add(tag)

            for pic in formset:
                try:
                    picture = Picture(image = pic.cleaned_data['image'], project = project)
                    picture.save()
                except Exception as e:
                    break
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('Home'))

        # If this is a GET (or any other method) create the default form.
    else:
        form = ProjectModelForm()
        formset = PicFormset(queryset = Picture.objects.none())
    context = {
        'form': form,
        'user_inst': user_inst,
        'formset': formset,
    }

    return render(request, 'first_form.html', context)


def show_project(request, pro_id):
    project = get_object_or_404(Project, pk=pro_id)
    if request.method == 'POST':
        comment_form = CommentModelForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = get_object_or_404(User, pk=5)  # will be replaced with session user
            comment.project = project
            comment.save()
            return HttpResponseRedirect(reverse('show_project', args=[project.id]))
    else:
        pics = project.picture_set.all
        rate = project.rate_set.all().aggregate(Avg('rate'))
        comment_form = CommentModelForm()
        context = {'project': project, 'pics': pics, 'rate': rate['rate__avg'], 'form': comment_form}
        return  render(request, 'show_project.html', context)

