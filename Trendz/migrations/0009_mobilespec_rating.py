# Generated by Django 3.1 on 2021-06-18 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trendz', '0008_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobilespec',
            name='rating',
            field=models.IntegerField(null=True),
        ),
    ]
