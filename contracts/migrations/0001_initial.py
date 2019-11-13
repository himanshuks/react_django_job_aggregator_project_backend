# Generated by Django 2.2.5 on 2019-10-30 06:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=200, unique=True)),
                ('company_logo_url', models.URLField(blank=True, default='https://c.yell.com/t_bigRect,f_auto/ccd850d5-3dde-43b4-bc01-6b41afdc4161_image_png.png', max_length=2000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(blank=True, max_length=200, unique=True)),
                ('source_logo_url', models.URLField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default='Title not available')),
                ('posted_datetime', models.DateTimeField(blank=True, null=True)),
                ('salary', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('rating', models.IntegerField(default=-1)),
                ('url', models.URLField(max_length=2000, unique=True)),
                ('categories', models.ManyToManyField(blank=True, related_name='contracts', to='contracts.Category')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracts', to='contracts.Company')),
                ('domains', models.ManyToManyField(blank=True, related_name='contracts', to='contracts.JobDomain')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracts', to='contracts.Location')),
                ('skills', models.ManyToManyField(blank=True, related_name='contracts', to='contracts.Skill')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='contracts.Source')),
            ],
        ),
    ]
