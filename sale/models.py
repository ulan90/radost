from django.db import models
from goods.models import Good

# Create your models here.
class SoldGoods(models.Model):
    receipt_id = models.IntegerField(null=True, blank=True)
    good = models.ForeignKey(Good, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    sold_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    sold_sum = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.good)