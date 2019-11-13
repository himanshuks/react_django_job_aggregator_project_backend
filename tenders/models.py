from django.db import models


# Create your models here.
class Location(models.Model):

    location_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.location_name


class Status(models.Model):

    tender_status = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.tender_status


class TenderSource(models.Model):

    tender_source = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.tender_source


class Category(models.Model):

    tender_category_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.tender_category_name


class Tender(models.Model):

    title = models.TextField()
    value = models.CharField(max_length=200)
    url = models.URLField(max_length=2000, unique=True)
    closing_datetime = models.DateTimeField(null=True, blank=True)
    published_datetime = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(default=-1)
    is_for_free_users = models.BooleanField(default=False)

    category = models.ForeignKey(Category, related_name='tenders', on_delete=models.SET_NULL, null=True, blank=True)
    source = models.ForeignKey(TenderSource, related_name='tenders', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, related_name='tenders', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, related_name='tenders', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
