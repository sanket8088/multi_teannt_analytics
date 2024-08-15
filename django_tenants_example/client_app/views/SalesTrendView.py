from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from client_app.models import SalesData
from client_app.serializers import SalesTrendsSerializer
import datetime

class SalesTrendsView(generics.GenericAPIView):
    """
    API endpoint that retrieves sales trends for a specific product over a given period.

    Input:
        POST request body (application/json):
            - product_id (int): The ID of the product for which to retrieve sales trends.
            - start_date (date): The start date in YYYY-MM format.
            - end_date (date): The end date in YYYY-MM format.

    Output:
        - success (bool): Indicates if the request was successful.
        - data (list): List of dictionaries, each containing:
            - total_sales (float): Total sales amount for the month.

    Errors:
        - 400: Bad request with validation errors.
        - 404: No sales data found for the specified period.
        - 500: Internal server error with error details.
    """

    serializer_class = SalesTrendsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response_data = {
                "success": False,
                "error": serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_id = serializer.validated_data['product_id']
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date'] + datetime.timedelta(days=31)

            sales_trends = SalesData.objects.filter(
                product_id=product_id,
                sale_date__range=[start_date, end_date]
            ).annotate(month=TruncMonth('sale_date')) \
             .values('month') \
             .annotate(total_sales=Sum('amount')) \
             .order_by('month')

            if not sales_trends:
                response_data = {
                    "success": False,
                    "error": "No sales data found for the specified period."
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            # Extract only total_sales from the data
            total_sales_data = [{"total_sales": entry["total_sales"]} for entry in sales_trends]
            response_data = {
                "success": True,
                "data": total_sales_data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                "success": False,
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
