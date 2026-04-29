import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from lessons.models import Lesson

replacements = {
    "Backend qismida": "backend qismida",
    "Ma'lumotlarni tahlil qilish": "ma'lumotlarni tahlil qilish",
    "Kundalik zerikarli ishlarni": "kundalik zerikarli ishlarni",
    "Birinchi Dasturingiz: 'Salom, Dunyo!'": "Birinchi dasturingiz: 'Salom, dunyo!'",
    "For Tsikli": "For tsikli",
    "While Tsikli": "While tsikli",
}

for l in Lesson.objects.all():
    new_content = l.content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != l.content:
        l.content = new_content
        l.save()
        print(f"Updated content for Lesson: {l.title}")

from lessons.models import Task
task_replacements = {
    "Matnlarni qo'shish (Konkatenatsiya)": "Matnlarni qo'shish (konkatenatsiya)",
    "Juft yoki Toq": "Juft yoki toq",
    "Salom Dunyo": "Salom dunyo"
}

for t in Task.objects.all():
    new_title = t.title
    for old, new in task_replacements.items():
        new_title = new_title.replace(old, new)
    if new_title != t.title:
        t.title = new_title
        t.save()
        print(f"Updated Task title: {t.title}")

print("Done")
