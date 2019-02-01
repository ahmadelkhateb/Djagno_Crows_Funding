from django.forms import ModelForm
from Projects.models import Project


class ProjectModelForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_date', 'end_date', 'tags']

