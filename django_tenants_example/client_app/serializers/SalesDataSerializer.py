from rest_framework import serializers

class SalesDataSerializer(serializers.Serializer):
    month = serializers.DateField(format="%Y-%m")
    avg_sales = serializers.FloatField()


class SalesTrendsDataSerializer(serializers.Serializer):
    month = serializers.DateField(format="%Y-%m")
    total_sales = serializers.FloatField()