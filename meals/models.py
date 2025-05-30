from django.db import models
from django.conf import settings
from inventory.models import Product
from django.core.exceptions import ValidationError
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Meal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_possible_portions(self):
        """Har bir taom uchun mumkin bo‘lgan porsiyalarni hisoblaydi."""
        logger.info(f"Calculating possible portions for Meal {self.id} - {self.name}")
        if not self.ingredients.exists():
            logger.warning(f"No ingredients found for Meal {self.id}")
            return 0
        # Har bir ingredient uchun mavjud porsiyalarni hisoblash
        portions = []
        for ingredient in self.ingredients.all():
            if ingredient.quantity_grams <= 0:
                logger.warning(f"Ingredient {ingredient.id} for Meal {self.id} has quantity_grams <= 0: {ingredient.quantity_grams}")
                return 0
            if ingredient.product.quantity_grams <= 0:
                logger.warning(f"Product {ingredient.product.id} for Ingredient {ingredient.id} has quantity_grams <= 0: {ingredient.product.quantity_grams}")
                return 0
            # Ingredient uchun zarur miqdor (quantity_grams) asosida porsiyalar
            available_portions = ingredient.product.quantity_grams // ingredient.quantity_grams
            logger.info(f"Ingredient {ingredient.id}: {ingredient.product.quantity_grams}g available, {ingredient.quantity_grams}g per portion, portions: {available_portions}")
            portions.append(available_portions)
        # Eng kam porsiya sonini olish (cheklovchi ingredient)
        result = int(min(portions)) if portions else 0
        logger.info(f"Possible portions for Meal {self.id}: {result}")
        return result

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Ingredient(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='ingredients')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_grams = models.FloatField()

    def __str__(self):
        return f"{self.meal.name} - {self.product.name}"

class MealDistribution(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='meal_distributions'
    )
    date_time = models.DateTimeField()
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        for ingredient in self.meal.ingredients.all():
            required = ingredient.quantity_grams * self.quantity
            if ingredient.product.quantity_grams < required:
                raise ValidationError(f"{ingredient.product.name} yetarli emas.")
            ingredient.product.quantity_grams -= required
            ingredient.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.meal.name} - {self.quantity} porsiya"