# Generated by Django 3.1 on 2021-06-29 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trendz', '0013_laptopcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='link',
            field=models.CharField(max_length=50, null=True),
        ),
    ]