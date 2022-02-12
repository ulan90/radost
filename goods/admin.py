from django.contrib import admin
from .models import Author, PublishingHouse, Group, Genre, Good, Barcode, Balance, IzlishkiTovara

# Register your models here.
admin.site.register(Author)
admin.site.register(PublishingHouse)
admin.site.register(Group)
admin.site.register(Genre)
admin.site.register(Good)
admin.site.register(Barcode)
admin.site.register(Balance)
admin.site.register(IzlishkiTovara)