import os, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from courses.models import Course
from lessons.models import Lesson

# 1. Kurs nomidan "(to'liq kurs)" ni olib tashlash
for c in Course.objects.all():
    old = c.title
    c.title = c.title.replace(" (to'liq kurs)", '').replace(' (toliq kurs)', '').strip()
    if old != c.title:
        print(f"Kurs nomi: {old!r} -> {c.title!r}")
    c.save()

# 2. Birinchi kurs tavsifini yangilash
c1 = Course.objects.first()
if c1:
    c1.description = "Python dasturlash asoslarini noldan o'rganish uchun mo'ljallangan o'quv qo'llanma"
    c1.save()
    print(f"Tavsif yangilandi: {c1.title!r}")

# 3. Dars nomlarida "Python" -> "python" (gapning boshida emas)
for l in Lesson.objects.all():
    # "Kirish va Python haqida" -> "Kirish va python haqida"
    # Regex: Python so'zi gapning boshida bo'lmagan joyda (raqam. dan keyin ham kichik bo'lishi kerak)
    new_title = re.sub(r'(?<!\A)(?<!\. )Python', 'python', l.title)
    # Agar raqam bilan boshlansa (masalan "1. Kirish va Python"), ham kichik
    new_title = re.sub(r'(\d+\.\s+\S.*?\s)Python', lambda m: m.group(0).replace('Python', 'python'), new_title)
    if new_title != l.title:
        print(f"Dars: {l.title!r} -> {new_title!r}")
        l.title = new_title
        l.save()

print("Hammasi tayyor!")
