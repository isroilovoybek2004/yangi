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
    
    # Ensure roles and users are properly configured in database
    try:
        from setup_roles import setup_roles
        setup_roles()
    except Exception as re:
        print("Setup roles failed:", re)
    
    # Check if database is empty to run seeders
    from courses.models import Course
    from lessons.models import Lesson
    if not Course.objects.exists():
        from tmp.populate_data import populate as pop_data
        from tmp.populate_skeleton import populate as pop_skeleton
        
        pop_data()
        pop_skeleton()
        try:
            call_command("seed_quizzes", force=True)
        except Exception as ex:
            print("Quiz seeding failed:", ex)
        try:
            call_command("seed_badges", interactive=False)
        except Exception:
            pass
            
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin123")

    # Seed quizzes if they are missing for some lessons
    try:
        from lessons.models import Lesson, Quiz
        if Lesson.objects.exists() and Quiz.objects.count() < Lesson.objects.count():
            print("Missing quizzes detected. Auto seeding quizzes...")
            call_command("seed_quizzes", force=True)
    except Exception as qe:
        print("Auto seeding missing quizzes failed:", qe)

    # Seed missing tasks for Lesson 10 if they are missing
    try:
        from lessons.models import Lesson, Task
        lesson10 = Lesson.objects.filter(title__icontains="10.").first() or Lesson.objects.filter(order=10).first()
        if lesson10 and Task.objects.filter(lesson=lesson10).count() < 3:
            print("Missing Lesson 10 tasks detected. Auto seeding tasks...")
            from seed_tasks import seed_missing_tasks
            seed_missing_tasks()
    except Exception as te:
        print("Auto seeding missing tasks failed:", te)
except Exception as e:
    print("Auto-migrate or seed failed:", e)
