from rest_framework import serializers
from reports.models import MonthlyReport

class MonthlyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyReport
        fields = ['id', 'month', 'prepared_portions', 'possible_portions', 'difference_percent', 'warning']
        read_only_fields = ['id', 'difference_percent', 'warning']
    def validate_prepared_portions(self, value):
        if value < 0:
            raise serializers.ValidationError("Tayyorlangan porsiyalar musbat bo‘lishi kerak.")
        return value
    def validate_possible_portions(self, value):
        if value < 0:
            raise serializers.ValidationError("Mumkin bo‘lgan porsiyalar musbat bo‘lishi kerak.")
        return value