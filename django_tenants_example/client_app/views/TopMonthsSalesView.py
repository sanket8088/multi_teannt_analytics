from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Avg
from django.db.models.functions import TruncMonth
from client_app.models import SalesData
from client_app.serializers import SalesDataSerializer

class TopMonthsView(generics.GenericAPIView):
    """
    API endpoint that retrieves the top 3 months with the highest average sales.

    Input:
        No query parameters or request body required.

    Output:
        - success (bool): Indicates if the request was successful.
        - data (list): List of dictionaries containing:
            - month (str): Month in YYYY-MM format.
            - avg_sales (float): Average sales amount for that month.

    Errors:
        - 404: No sales data found.
        - 500: Internal server error with error details.
    """

    def get(self, request):
        try:
            # Calculate sales per month and average sales
            sales_per_month = SalesData.objects.annotate(month=TruncMonth('sale_date')) \
                                               .values('month') \
                                               .annotate(avg_sales=Avg('amount')) \
                                               .order_by('-avg_sales')[:3]

            if not sales_per_month:
                response_data = {
                    "success": False,
                    "error": "No sales data found."
                }
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            sales_data_serializer = SalesDataSerializer(sales_per_month, many=True)
            response_data = {
                "success": True,
                "data": sales_data_serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                "success": False,
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
