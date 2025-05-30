import pytest
from inventory.models import Product

@pytest.mark.django_db
def test_check_low_stock_true():
    # Min miqdordan kam bo'lsa: low stock True bo'lishi kerak
    product = Product.objects.create(
        name="Un",
        quantity_grams=10,
        min_quantity=20
    )
    assert product.check_low_stock() is True

@pytest.mark.django_db
def test_check_low_stock_false():
    # Min miqdordan ko'p bo'lsa: low stock False bo'lishi kerak
    product = Product.objects.create(
        name="Yog'",
        quantity_grams=50,
        min_quantity=20
    )
    assert product.check_low_stock() is False

@pytest.mark.django_db
def test_check_low_stock_equal():
    # Miqdor aynan minimalga teng bo'lsa ham low stock True bo'lishi kerak
    product = Product.objects.create(
        name="Tuz",
        quantity_grams=20,
        min_quantity=20
    )
    assert product.check_low_stock() is True