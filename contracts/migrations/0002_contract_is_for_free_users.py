# Generated by Django 2.2.5 on 2019-11-04 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='is_for_free_users',
            field=models.BooleanField(default=False),
        ),
    ]