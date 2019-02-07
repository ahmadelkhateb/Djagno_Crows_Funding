from django.forms import ModelForm, TextInput
from Projects.models import Project, Tag, Comment, Rate, ReportComment, ReportProject, Donation


class ProjectModelForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'start_date', 'end_date', ]
        widgets = {
            'start_date': TextInput(attrs={'type': 'date'}),
            'end_date': TextInput(attrs={'type': 'date'}),
        }


class TagModelForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['tag', ]


class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', ]


class RateModelForm(ModelForm):
    class Meta:
        model = Rate
        fields = ['rate', ]


class ReportProjectForm(ModelForm):
    class Meta:
        model = ReportProject
        fields = ['reason', ]


class ReportCommentForm(ModelForm):
    class Meta:
        model = ReportComment
        fields = ['reason', ]


class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ['amount', ]
