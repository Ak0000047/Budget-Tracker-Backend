import os
from django.core.wsgi import get_wsgi_application

# Run migrations automatically on app startup
def run_migrations():
    import django
    django.setup()

    from django.core.management import call_command

    try:
        call_command('migrate', interactive=False)
        print("Migrations applied successfully.")
    except Exception as e:
        print(f"Error applying migrations: {e}")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

run_migrations()

application = get_wsgi_application()
