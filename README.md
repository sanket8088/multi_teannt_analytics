# Sales analytics multi-tenant DB

## Project Description
This project is designed for managing and analyzing sales data within a multi-tenant environment. It provides functionalities to insert sales data and perform various analyses through a set of APIs. The system supports multiple tenants, each with its own isolated schema within the database, allowing for separate data management and analysis for different clients or business units.

## Key features include:

Data Insertion: Import sales data from CSV files into the system.
Data Analysis: Use APIs to analyze and retrieve sales trends and metrics.
Multi-Tenancy Support: Manage data for multiple tenants with isolated schemas.
The project leverages Celery for handling background tasks, ensuring smooth data processing and analysis.

## Installation

Clone the project from github
```bash
git clone <repository-url>
cd <repository-directory>
```

Create and activate a virtual env
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Install Dependencies
```bash
pip install -r requirements.txt
```

## Craeting a .env file

There is a .env.sample file present which needs DB secured information (Use postgresql as DB here). Create a .env and add all the required info to make db connection

## Running the project

1. Migrate and create shared schemas
```bash
python manage.py migrate_schemas --shared
```

2. Creating a tenant
Run this command to open interactive shell in dajngo
```bash
python manage.py shell
```

Now use the following code after updating it based on your need

```python
from app.models import Client, Domain
# Recommend to create a public schema first
tenant = Client(schema_name="public", name="Public")
tenant.save()
domain = Domain(domain="localhost", tenant = tenant, is_primary=True)
domain.save()
# Dont change code till here.
# Start updating your code from here  
tenant = Client(schema_name="abc_comp", name="Abc")
tenant.save()
domain = Domain(domain="abc.localhost", tenant = tenant, is_primary=True)
domain.save()
exit()
```

Once you exit you should have abc_comp schema created in your db.

3. Migration
There are two commands to create migrations.

Case 1:- Migration for only schema
```bash
python manage.py migrate_schemas --schema=abc_comp
```

Case 2:- Migrate for all schema (Recommended) - This is a custom manangement command and can be found in app.management
```bash
 python manage.py migrate_all_tenants
```

4. Run the server
```bash
python manage.py runserver
```
Verify the link http://abc.localhost:8000/ where abc is the name domain passed while creating the tenant

## Loading data in db

There are csv in data_ingestion folder. To load data in db run following command
```bash
python manage.py load_data_from_csv abc_comp
```

**Please note abc_comp is the name of schema or tenant in which I want to load data**

## Running celery for scheduled task to reload data every 24 hrs
Run the command to start the celery worker
```bash
celery -A project worker --loglevel=info

```

Run the below command to start celery beat which is responsible for scheduling the tasks at 24 hrs interval
```bash
celery -A project beat --loglevel=info
```

## Verify the API's
In the project root directory there is openapi_spec.yaml file which has the swagger doc. Copy the file and open [swagger editor](https://editor.swagger.io/).
Paste the whole file data in the editor to view API Documentation.
Also curls.sh file added for directly accessing curl requests.
