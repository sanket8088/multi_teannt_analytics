# app/tasks.py
from celery import shared_task
import csv
from django_tenants.utils import schema_context
from app.models import Product, Customer, SalesData

@shared_task
def refresh_data_task(schema_name, csv_file):
    """
    Refresh data in the database from the specified CSV file.

    Args:
        schema_name (str): The schema name of the tenant to refresh data for.
        csv_file (str): The path to the CSV file with data.
    """
    with schema_context(schema_name):
        # Refresh products
        load_csv(csv_file, Product, ['id', 'name'])

        # Refresh customers
        load_csv(csv_file, Customer, ['id', 'name', 'email'])

        # Refresh sales data
        load_sales_data(csv_file)

def load_csv(file_name, model, fields):
    """
    Load data from a CSV file into a Django model.

    Args:
        file_name (str): The path to the CSV file.
        model (Django model): The model to load data into.
        fields (list): The list of fields to map from CSV to model.
    """
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data = {field: row[field] for field in fields}
            model.objects.update_or_create(**data)

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
