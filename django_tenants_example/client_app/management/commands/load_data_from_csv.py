import csv
from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from client_app.models import Product, Customer, SalesData

class Command(BaseCommand):
    """
    Command to load data from CSV files into tenant models.

    Arguments:
        schema_name (str): The schema name of the tenant to load data into.
        --incremental (optional): Load data incrementally (default: false).

    The command will load data into the following models:
        - Product
        - Customer
        - SalesData
    """

    help = 'Load data from CSV files into tenant models'

    def add_arguments(self, parser):
        parser.add_argument(
            'schema_name',
            type=str,
            help='The schema name of the tenant to load data into'
        )
        parser.add_argument(
            '--incremental',
            action='store_true',
            help='Load data incrementally (default: false)'
        )

    def handle(self, *args, **options):
        schema_name = options['schema_name']
        is_incremental = options['incremental']

        with schema_context(schema_name):
            # Load products
            self.load_csv('data_ingestion/Product.csv', Product, ['id', 'name'])

            # Load customers
            self.load_csv('data_ingestion/Customer.csv', Customer, ['id', 'name', 'email'])

            # Load sales data
            sales_data_file = 'data_ingestion/SalesData_1.csv'
            self.load_sales_data(sales_data_file)

    def load_csv(self, file_name, model, fields):
        """
        Load data from a CSV file into a Django model.

        Args:
            file_name (str): The path to the CSV file.
            model (django.db.models.Model): The Django model to load data into.
            fields (list of str): The fields of the model to be populated from the CSV file.
        """
        with open(file_name, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data = {field: row[field] for field in fields}
                model.objects.update_or_create(**data)

    def load_sales_data(self, file_name):
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
