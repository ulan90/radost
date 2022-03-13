from django.db import models
from goods.models import Good

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class AcceptanceDocs(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    doc_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name_plural = "Acceptance documents"


class AcceptanceGoods(models.Model):
    good = models.ForeignKey(Good, on_delete=models.SET_NULL, null=True, blank=True)
    doc_id = models.ForeignKey(AcceptanceDocs, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.good)
    
    class Meta:
        verbose_name_plural = "Acceptance goods"


class SupplierPrice(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE, null=False, blank=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.good)