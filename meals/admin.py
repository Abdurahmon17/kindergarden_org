from django.contrib import admin
from .models import Meal, Ingredient, MealDistribution

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'name': ('name',)}  # Forma uchun avtomatik to‘ldirish

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('meal', 'product', 'quantity_grams')
    list_filter = ('meal', 'product')
    search_fields = ('meal__name', 'product__name')
    ordering = ('meal',)

@admin.register(MealDistribution)
class MealDistributionAdmin(admin.ModelAdmin):
    list_display = ('meal', 'user', 'date_time', 'quantity')
    list_filter = ('meal', 'user', 'date_time')
    search_fields = ('meal__name', 'user__username')
    ordering = ('-date_time',)