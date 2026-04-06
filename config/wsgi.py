"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

app = application

# Auto-migrate and Seed for Vercel deployment on new DBs
try:
    from django.core.management import call_command
    call_command("migrate", interactive=False)
    
    # Check if database is empty to run seeders
    from courses.models import Course
    if not Course.objects.exists():
        from tmp.populate_data import populate as pop_data
        from tmp.populate_skeleton import populate as pop_skeleton
        
        pop_data()
        pop_skeleton()
        try:
            call_command("seed_badges", interactive=False)
        except Exception:
            pass
            
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")
except Exception as e:
    print("Auto-migrate or seed failed:", e)
