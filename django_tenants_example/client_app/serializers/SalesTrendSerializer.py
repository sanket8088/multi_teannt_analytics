from rest_framework import serializers

class SalesTrendsSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255)
    start_date = serializers.DateField(format='%Y-%m')
    end_date = serializers.DateField(format='%Y-%m')
