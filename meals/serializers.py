from rest_framework import serializers
from meals.models import Ingredient
from inventory.models import Product
from rest_framework import serializers
from meals.models import Meal
from django.utils import timezone
from meals.models import MealDistribution

class IngredientSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = Ingredient
        fields = ['product', 'quantity_grams']
    def validate_quantity_grams(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ingredient miqdori musbat bo‘lishi kerak.")
        return value

class MealSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    possible_portions = serializers.SerializerMethodField()
    class Meta:
        model = Meal
        fields = ['id', 'name', 'ingredients', 'possible_portions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    def get_possible_portions(self, obj):
        return obj.calculate_possible_portions()
    def validate_name(self, value):
        if Meal.objects.filter(name=value).exists() and self.instance is None:
            raise serializers.ValidationError("Bu ovqat nomi allaqachon mavjud.")
        return value
    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError("Kamida bitta ingredient kiritilishi kerak.")
        return value
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        meal = Meal.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(meal=meal, **ingredient_data)
        return meal
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        instance.ingredients.all().delete()
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(meal=instance, **ingredient_data)
        return instance


class MealDistributionSerializer(serializers.ModelSerializer):
    meal = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all())
    user = serializers.StringRelatedField(read_only=True)
    date_time = serializers.DateTimeField(read_only=True, default=timezone.now)
    class Meta:
        model = MealDistribution
        fields = ['id', 'meal', 'user', 'date_time', 'quantity']
        read_only_fields = ['id', 'user', 'date_time']
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Porsiyalar soni musbat bo‘lishi kerak.")
        return value
    def validate(self, data):
        meal = data['meal']
        quantity = data['quantity']
        for ingredient in meal.ingredients.all():
            required = ingredient.quantity_grams * quantity
            if ingredient.product.quantity_grams < required:
                raise serializers.ValidationError(
                    f"{ingredient.product.name} yetarli emas: {required}g kerak, {ingredient.product.quantity_grams}g mavjud."
                )
        return data
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)