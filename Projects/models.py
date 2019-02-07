from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    
class Project(models.Model):
    title = models.CharField(max_length=50)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_target = models.IntegerField('Total Target')
    start_date = models.DateField()
    end_date = models.DateField()
    tags = models.ManyToManyField('Tag')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def total_donations_check(self):
        total = 0
        for donate in self.donation_set.all():
            total += donate.amount
        return total < (self.total_target / 4)

    def donation_percent(self):
        total = 0
        for donate in self.donation_set.all():
            total += donate.amount
        return int((total / self.total_target) * 100)

    def first_image(self):
        return self.picture_set.all()[:1]

    def similar_projects(self):
        project_tags = self.tags.all()
        similar = Project.objects.none()
        for tag in project_tags:
            project_list = tag.project_set.all()
            similar = (similar | project_list)
        return similar.distinct()[:6]


class Picture(models.Model):
    image = models.ImageField(upload_to="Projects/images", null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag

    def tag_exists(self,name):
        return self.objects.get(tag=name)


class Donation(models.Model):
    amount = models.PositiveIntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.project) + str(self.amount)


class Comment(models.Model):
    comment = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class ReportComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reason


class ReportProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reason = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reason


class Rate(models.Model):
    rate = models.IntegerField(validators=[MaxValueValidator(5, message="Max Rate Value is 5",),
                                           MinValueValidator(1, message="Min Rate value is 1")],)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'project'),)

    def __str__(self):
        return str(self.project) + "By : " + str(self.user) + " : " + str(self.rate)

