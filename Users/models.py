from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Users/images")
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=11, validators=[RegexValidator(regex='^01[0|1|2|5][0-9]{8}$',
                                            message="Phone number must be : 010 or 011 or 012 or 015.",
                                            code="Invalid Phone Number")])
    facebook_profile = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


