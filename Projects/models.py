from django.db import models
from Users.models import User
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


class Picture(models.Model):
    image = models.ImageField(upload_to="Projects/static/Projects/images", null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Tag(models.Model):
    tag = models.CharField(max_length=50)

    def __str__(self):
        return self.tag

class Donation(models.Model):
    amount = models.PositiveIntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.title, self.amount

class Comment(models.Model):
    comment = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

class Report_comment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reason = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reason


class Report_project(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reason = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reason


class Rate(models.Model):
    rate = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'project'),)

    def __str__(self):
        return str(self.project) + "By : " + str(self.user) + " : " + str(self.rate)



