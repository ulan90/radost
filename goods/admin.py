from django.contrib import admin
from .models import Author, PublishingHouse, Group, Genre, Good

# Register your models here.
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Group)
admin.site.register(Genre)
admin.site.register(Good)