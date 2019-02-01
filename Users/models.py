from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class User(models.Model):
    first_name = models.CharField("First Name", max_length=50)
    last_name = models.CharField("Last Name", max_length=50)
    email = models.EmailField(max_length=70)
    password = models.CharField(max_length=8)
    phone = models.IntegerField(validators=[RegexValidator(regex='^1[0|1|2|5][0-9]{8}$',
                                                        message="Phone number must be : 010 or 011 or 012 or 015.",
                                                         code="Invalid Phone Number")])
    pic = models.ImageField(upload_to="Users/static/Users/images")

    def __str__(self):
        return self.first_name+ " " + self.last_name
