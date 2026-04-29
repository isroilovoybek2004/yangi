import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from lessons.models import Quiz, Task, Lesson

# Fix Quiz Titles
for q in Quiz.objects.all():
    title = q.title
    if " — Nazariy test" in title:
        q.title = title.replace(" — Nazariy test", " — nazariy test")
        q.save()
        print(f"Updated Quiz: {q.title}")

# Fix Task Titles
# Some tasks start with capital letter, we will lower case them if they follow "Topshiriq: "
# Actually, the frontend renders "Topshiriq: " + task.title.
# Let's lowercase the first letter of task titles to make it sentence case when concatenated.
# E.g., "Birinchi qadam" -> "birinchi qadam"
for t in Task.objects.all():
    title = t.title
    if title and title[0].isupper():
        new_title = title[0].lower() + title[1:]
        t.title = new_title
        t.save()
        print(f"Updated Task: {t.title}")

# Also check seed_quizzes.py and seed_lessons.py
