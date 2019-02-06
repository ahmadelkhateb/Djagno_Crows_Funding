from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from Projects.models import Project, Picture, Tag, Comment
from Projects.forms import ProjectModelForm, CommentModelForm, RateModelForm, ReportProjectForm, ReportCommentForm, DonationForm
from django.forms import modelformset_factory
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    return HttpResponse("You Did It Sasuke")


@login_required
def first_form(request):
    PicFormset = modelformset_factory(Picture, fields=('image',), extra=4)
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = ProjectModelForm(request.POST)
        formset = PicFormset(request.POST,request.FILES)
        # Check if the form is valid:
        if form.is_valid() and formset.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            tags_str = request.POST['tag'].split(',')
            for tag in tags_str:
                tag = tag.lower()
                try:
                    Tag.objects.get(tag=tag)
                except ObjectDoesNotExist:
                    tag = Tag(tag=tag)
                    tag.save()
                    project.tags.add(tag)
                else:
                    tag = Tag.objects.get(tag=tag)
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
        # sess_user = request.session['_auth_user_id']
    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'first_form.html', context)


@login_required
def show_project(request, pro_id):
    project = get_object_or_404(Project, pk=pro_id)
    pics = project.picture_set.all
    rate = project.rate_set.all().aggregate(Avg('rate'))
    comments = project.comment_set.all()
    #similars = project.objects.filter
    if request.method == 'POST':
        comment_form = CommentModelForm(request.POST)
        rate_form = RateModelForm(request.POST)
        donation_form = DonationForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.project = project
            comment.save()
            messages.success(request, 'Your Comment has been added')
            return HttpResponseRedirect(reverse('show_project', args=[project.id]))

        elif rate_form.is_valid():
            rate = rate_form.save(commit=False)
            rate.user = request.user
            rate.project = project
            rate.save()
            messages.success(request, 'Thank you for your time')
            return HttpResponseRedirect(reverse('show_project', args=[project.id]))

        elif donation_form.is_valid():
            donate = donation_form.save(commit=False)
            donate.user = request.user
            donate.project = project
            donate.save()
            messages.success(request, 'Thank you for your Donation')
            return HttpResponseRedirect(reverse('show_project', args=[project.id]))
    else:
        comment_form = CommentModelForm()
        rate_form = RateModelForm()
        donation_form = DonationForm()
    context = {'project': project, 'pics': pics, 'rate': rate['rate__avg'],
               'form': comment_form, 'comments': comments, 'rate_form': rate_form, 'donate': donation_form}
    return  render(request, 'show_project.html', context)


@login_required
def add_report(request, pro_id):
    project = get_object_or_404(Project, pk=pro_id)
    if request.method == 'POST':
        report_form = ReportProjectForm(request.POST)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.user = request.user
            report.project = project
            report.save()
            messages.success(request, 'Your Report has been added, Sorry for disrupting you')
            return HttpResponseRedirect(reverse('show_project', args=[project.id]))
    else:
        report_form = ReportProjectForm()
        context = {'form': report_form, 'project': project}
        return render(request, 'report.html', context)


@login_required
def add_report_comment(request, com_id):
    comment = get_object_or_404(Comment, pk=com_id)
    if request.method == 'POST':
        report_form = ReportCommentForm(request.POST)
        if report_form.is_valid():
            report = report_form.save(commit=False)
            report.user = request.user
            report.comment = comment
            report.save()
            messages.success(request, 'Your Report has been added, Sorry for disrupting you')
            return HttpResponse("Your Report has been delieverd . thank you for your time")
    else:
        report_form = ReportCommentForm()
        context = {'form': report_form, 'comment': comment}
        return render(request, 'report.html', context)

