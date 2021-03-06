# Generated by Django 2.2.5 on 2019-10-31 06:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tenders', '0001_initial'),
        ('contracts', '0001_initial'),
        ('bookmarks', '0002_auto_20191030_0622'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookmarkedcontract',
            unique_together={('contract', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='bookmarkedtender',
            unique_together={('tender', 'user')},
        ),
    ]
