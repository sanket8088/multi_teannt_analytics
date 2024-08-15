from django.core.management.base import BaseCommand
from django.core.management import call_command
from app.models import Client

class Command(BaseCommand):
    """
    Command to apply migrations to all tenant schemas.

    This command retrieves all tenant schemas from the Client model and applies
    migrations to each tenant schema individually. It uses the `migrate_schemas`
    management command to apply the migrations.

    Usage:
        python manage.py migrate_all_tenants
    """

    help = 'Apply migrations to all tenant schemas'

    def handle(self, *args, **kwargs):
        """
        Retrieve all tenant schemas and apply migrations to each schema.

        For each tenant schema found in the Client model:
            - Retrieve the schema name.
            - Apply migrations using the `migrate_schemas` command.

        If no tenant schemas are found, a notice is displayed.
        """
        # List all tenant schemas
        tenants = Client.objects.all()
        if not tenants.exists():
            self.stdout.write(self.style.NOTICE('No tenants found.'))
            return

        for tenant in tenants:
            schema_name = tenant.schema_name
            self.stdout.write(self.style.SUCCESS(f'Applying migrations for schema: {schema_name}'))
            call_command('migrate_schemas', schema_name=schema_name)
            
        self.stdout.write(self.style.SUCCESS('Migrations applied to all tenant schemas.'))



# Do a migraton using python manage.py migrate_all_tenants
