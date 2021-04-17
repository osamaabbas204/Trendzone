# Generated by Django 3.1.7 on 2021-03-31 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('purpose', models.CharField(choices=[('IN', 'Inquiry'), ('CO', 'Complaint'), ('FB', 'Feedback')], max_length=2)),
                ('message', models.TextField()),
            ],
        ),
    ]