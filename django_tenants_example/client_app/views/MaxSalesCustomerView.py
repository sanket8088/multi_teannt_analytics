from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils.dateparse import parse_date
import datetime
from client_app.models import SalesData

class MaxSalesCustomerView(generics.GenericAPIView):
    """
    API endpoint that retrieves the customer with the maximum sales per month for a given period.

    Input:
        Query parameters:
            - start_date (str): The start date in YYYY-MM format.
            - end_date (str): The end date in YYYY-MM format.

    Output:
        - success (bool): Indicates if the request was successful.
        - data (dict): Dictionary where:
            - key: Month in YYYY-MM format.
            - value: Dictionary containing:
                - customer_id (int): The ID of the customer with the highest sales for that month.
                - total_sales (float): Total sales amount for the customer in that month.

    Errors:
        - 400: Missing required parameters or invalid date format.
        - 500: Internal server error with error details.
    """

    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        
        if not start_date_str or not end_date_str:
            return Response({
                'success': False,
                'error': 'Missing required parameters'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = parse_date(f"{start_date_str}-01")
            end_date = parse_date(f"{end_date_str}-01") + datetime.timedelta(days=31)

            monthly_sales = SalesData.objects.filter(
                sale_date__range=[start_date, end_date]
            ).annotate(month=TruncMonth('sale_date')) \
             .values('month', 'customer_id') \
             .annotate(total_sales=Sum('amount')) \
             .order_by('month')

            results = {}
            for entry in monthly_sales:
                month = entry['month'].strftime('%Y-%m')  # Convert to string format YYYY-MM
                customer_id = entry['customer_id']
                total_sales = entry['total_sales']
                
                if month not in results:
                    results[month] = {'customer_id': customer_id, 'total_sales': total_sales}
                else:
                    if total_sales > results[month]['total_sales']:
                        results[month] = {'customer_id': customer_id, 'total_sales': total_sales}
            
            response_data = {
                'success': True,
                'data': results
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError:
            return Response({
                'success': False,
                'error': 'Invalid date format'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
