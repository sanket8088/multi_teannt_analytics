from django.urls import path 

from client_app.views import TopMonthsView, SalesTrendsView, MaxSalesCustomerView

urlpatterns = [
    path('api/sales/top_months/', TopMonthsView.as_view(), name='top_months'),
    path('api/sales/trends/', SalesTrendsView.as_view(), name='sales_trends'),  # POST request for trends
    path('api/sales/max_sales_customer/', MaxSalesCustomerView.as_view(), name='max_sales_customer'),
]
