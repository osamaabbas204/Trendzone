# Generated by Django 3.1 on 2021-05-09 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trendz', '0004_specification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mobile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('price', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=200)),
                ('tag', models.CharField(max_length=200)),
                ('brand', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
    ]