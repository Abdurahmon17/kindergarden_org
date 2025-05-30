from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity_grams', 'min_quantity')  # Removed 'category'
    list_filter = ()  # Removed 'category' since it’s not a field
    search_fields = ('name',)
    list_editable = ('quantity_grams', 'min_quantity')
    ordering = ('name',)