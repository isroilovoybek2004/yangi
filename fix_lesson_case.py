import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from lessons.models import Lesson

replacements = {
    "1. Kirish va Python haqida tushuncha": "1. Kirish va Python haqida tushuncha", # looks ok
    "2. O'zgaruvchilar va Ma'lumot Turlari": "2. O'zgaruvchilar va ma'lumot turlari",
    "3. Shartli Operatorlar (if, elif, else)": "3. Shartli operatorlar (if, elif, else)",
    "4. Sikllar (for va while)": "4. Sikllar (for va while)",
    "5. Funksiyalar bilan ishlash": "5. Funksiyalar bilan ishlash",
    "6. Ma'lumotlar Tuzilmalari: Ro'yxatlar (List)": "6. Ma'lumotlar tuzilmalari: ro'yxatlar (list)",
    "7. Lug'atlar (Dictionary) bilan ishlash": "7. Lug'atlar (dictionary) bilan ishlash",
    "8. Python da OOP ga kirish": "8. Python da OOP ga kirish",
    "9. Modullar va paketlar": "9. Modullar va paketlar",
    "10. Xatolarni qayta ishlash (try-except)": "10. Xatolarni qayta ishlash (try-except)"
}

for l in Lesson.objects.all():
    if l.title in replacements:
        l.title = replacements[l.title]
        l.save()
        print(f"Updated Lesson: {l.title}")

