# Generated by Django 2.1.5 on 2019-02-05 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0003_auto_20190205_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='create_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]