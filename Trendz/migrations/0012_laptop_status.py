# Generated by Django 3.1 on 2021-06-24 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trendz', '0011_laptoptrend'),
    ]

    operations = [
        migrations.AddField(
            model_name='laptop',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
