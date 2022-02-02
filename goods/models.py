from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=50, null=False)
    parrent_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class PublishingHouse(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name

class Good(models.Model):
    name = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    Group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    Author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    published_house = models.ForeignKey(PublishingHouse, on_delete=models.SET_NULL, null=True, blank=True)
    Genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name