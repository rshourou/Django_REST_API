# Generated by Django 2.2.14 on 2020-08-13 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='origin',
        ),
        migrations.DeleteModel(
            name='Airport',
        ),
        migrations.DeleteModel(
            name='Flight',
        ),
    ]
