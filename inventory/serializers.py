from rest_framework import serializers
from inventory.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity_grams', 'delivery_date', 'min_quantity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    def validate_quantity_grams(self, value):
        if value < 0:
            raise serializers.ValidationError("Miqdor musbat bo‘lishi kerak.")
        return value
    def validate_min_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Minimal miqdor musbat bo‘lishi kerak.")
        return value
    def validate_name(self, value):
        if Product.objects.filter(name=value).exists() and self.instance is None:
            raise serializers.ValidationError("Bu nom allaqachon mavjud.")
        return value