from django.contrib import admin
from .models import Supplier, AcceptanceDocs, AcceptanceGoods, SupplierPrice

# Register your models here.
admin.site.register(Supplier)
admin.site.register(AcceptanceDocs)
admin.site.register(AcceptanceGoods)
admin.site.register(SupplierPrice)
