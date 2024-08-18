# app/tasks.py
from celery import shared_task
import csv
from django_tenants.utils import schema_context
from client_app.models import Product, Customer, SalesData

@shared_task
def refresh_data_task(schema_name, csv_file):
    """
    Refresh data in the database from the specified CSV file.

    Args:
        schema_name (str): The schema name of the tenant to refresh data for.
        csv_file (str): The path to the CSV file with data.
    """
    print("Running for schema name",schema_name )
    with schema_context(schema_name):
        # Refresh sales data
        load_sales_data(csv_file)

def load_sales_data(file_name):
    """
    Load sales data from a CSV file into the SalesData model.

    Args:
        file_name (str): The path to the CSV file.
    """
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            product = Product.objects.get(id=row['product_id'])
            customer = Customer.objects.get(id=row['customer_id'])
            SalesData.objects.update_or_create(
                product=product,
                customer=customer,
                sale_date=row['sale_date'],
                defaults={'amount': row['amount']}
            )

