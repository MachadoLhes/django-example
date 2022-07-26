from rest_framework import serializers

class RoundingDecimalField(serializers.DecimalField):
    def validate_precision(self, value):
        return value

class StockSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    symbol = serializers.CharField(max_length=20)
    open = RoundingDecimalField(max_digits=10, decimal_places=2)
    high = RoundingDecimalField(max_digits=10, decimal_places=2)
    low = RoundingDecimalField(max_digits=10, decimal_places=2)
    close = RoundingDecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateTimeField()
