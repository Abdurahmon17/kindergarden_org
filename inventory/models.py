from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity_grams = models.FloatField(default=0)
    delivery_date = models.DateField(default=timezone.now)
    min_quantity = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def check_low_stock(self):
        return self.quantity_grams <= self.min_quantity
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']