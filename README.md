# multi_teannt_analytics

 from app.models import Client, Domain
>>> tenant = Client(schema_name="public", name="Public")
>>> tenant.save()
>>> domain = Domain(domain="localhost", tenant = teannt, is_primary=True)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'teannt' is not defined
>>> domain = Domain(domain="localhost", tenant = teanant, is_primary=True)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
NameError: name 'teanant' is not defined
>>> domain = Domain(domain="localhost", tenant = tenant, is_primary=True)
>>> domain.save()
>>> tenant = Client(schema_name="abc_comp", name="Abc")
>>> tenant.save()
[1/1 (100%) standard:abc_comp] === Starting migration
[1/1 (100%) standard:abc_comp] Operations to perform:
[1/1 (100%) standard:abc_comp]   Apply all migrations: admin, app, auth, client_app, contenttypes, sessions
[1/1 (100%) standard:abc_comp] Running migrations:
[1/1 (100%) standard:abc_comp]   Applying contenttypes.0001_initial...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0001_initial...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying admin.0001_initial...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying admin.0002_logentry_remove_auto_add...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying admin.0003_logentry_add_action_flag_choices...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying app.0001_initial...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying contenttypes.0002_remove_content_type_name...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0002_alter_permission_name_max_length...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0003_alter_user_email_max_length...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0004_alter_user_username_opts...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0005_alter_user_last_login_null...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0006_require_contenttypes_0002...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0007_alter_validators_add_error_messages...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0008_alter_user_username_max_length...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0009_alter_user_last_name_max_length...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0010_alter_group_name_max_length...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0011_update_proxy_permissions...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying auth.0012_alter_user_first_name_max_length...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying client_app.0001_initial...
[1/1 (100%) standard:abc_comp]  OK
[1/1 (100%) standard:abc_comp]   Applying sessions.0001_initial...
[1/1 (100%) standard:abc_comp]  OK
>>> domain = Domain(domain="abc.localhost", tenant = tenant, is_primary=True)
>>> domain.save()
>>> exit()


Migrate

python manage.py migrate_schemas --schema=abc_comp
 1080  python manage.py migrate_all_tenants


python manage.py load_data_from_csv abc_comp - To insert data