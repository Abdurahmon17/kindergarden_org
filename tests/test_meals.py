import pytest
from meals.models import Meal, Ingredient
from inventory.models import Product

@pytest.mark.django_db
def test_calculate_possible_portions():
    # Productlar yaratamiz
    product1 = Product.objects.create(name="Kartoshka", quantity_grams=1000)
    product2 = Product.objects.create(name="Sabzi", quantity_grams=500)

    # Meal yaratamiz
    meal = Meal.objects.create(name="Osh")

    # Ingredientlar: 1 ta porsiya uchun 200g kartoshka, 100g sabzi kerak
    Ingredient.objects.create(meal=meal, product=product1, quantity_grams=200)
    Ingredient.objects.create(meal=meal, product=product2, quantity_grams=100)

    # Har bir ingredient uchun porsiya hisoblash:
    # Kartoshka: 1000 // 200 = 5
    # Sabzi: 500 // 100 = 5
    # Eng kichik qiymat: 5 porsiya
    assert meal.calculate_possible_portions() == 5

    # Agar ingredient yetarli bo‘lmasa, 0 qaytadi
    product1.quantity_grams = 100
    product1.save()
    assert meal.calculate_possible_portions() == 0