from django.forms import ModelForm
from Projects.models import Project, Tag, Comment


class ProjectModelForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_date', 'end_date', ]


class TagModelForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['tag', ]


class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', ]


