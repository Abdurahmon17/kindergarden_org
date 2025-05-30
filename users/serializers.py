from rest_framework import serializers
from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['id']
    def validate_role(self, value):
        if value not in dict(CustomUser.ROLE_CHOICES).keys():
            raise serializers.ValidationError("Noto‘g‘ri rol tanlandi.")
        return value