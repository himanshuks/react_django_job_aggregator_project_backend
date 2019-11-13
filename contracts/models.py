from django.db import models

# Create your models here.


class Category(models.Model):

    category_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.category_name.title()


class Location(models.Model):

    location_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.location_name.title()


class Skill(models.Model):

    skill_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.skill_name.title()


class JobDomain(models.Model):

    domain_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.domain_name.title()


class Company(models.Model):

    company_name = models.CharField(max_length=200, unique=True, blank=True)
    company_logo_url = models.URLField(
        max_length=2000,
        blank=True,
        null=True,
        default='https://c.yell.com/t_bigRect,f_auto/ccd850d5-3dde-43b4-bc01-6b41afdc4161_image_png.png'
    )

    def __str__(self):
        return self.company_name.title()


class Source(models.Model):

    source_name = models.CharField(max_length=200, unique=True, blank=True)
    source_logo_url = models.URLField(max_length=2000)

    def __str__(self):
        return self.source_name.title()


class Contract(models.Model):

    title = models.TextField(default='Title not available')
    posted_datetime = models.DateTimeField(null=True, blank=True)
    salary = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=-1)
    is_for_free_users = models.BooleanField(default=False)

    url = models.URLField(max_length=2000, unique=True)

    company = models.ForeignKey(Company, related_name='contracts', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, related_name='contracts', on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(Source, related_name='contracts', on_delete=models.CASCADE, null=True, blank=True)

    categories = models.ManyToManyField(Category, related_name='contracts', blank=True)
    skills = models.ManyToManyField(Skill, related_name='contracts', blank=True)
    domains = models.ManyToManyField(JobDomain, related_name='contracts', blank=True)

    def __str__(self):
        return f"{self.title}"
