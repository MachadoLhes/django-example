from rest_framework import serializers

class StockSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    symbol = serializers.CharField(max_length=20)
    open = serializers.DecimalField(max_digits=10, decimal_places=2)
    high = serializers.DecimalField(max_digits=10, decimal_places=2)
    low = serializers.DecimalField(max_digits=10, decimal_places=2)
    close = serializers.DecimalField(max_digits=10, decimal_places=2)