# Generated by Django 3.1.7 on 2021-04-01 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Trendz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='purpose',
        ),
    ]
