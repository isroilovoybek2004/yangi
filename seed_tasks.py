import os
import django

# Django environment setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from lessons.models import Lesson, Task

def seed_missing_tasks():
    print("=== Dars 10 uchun yetishmayotgan topshiriqlarni yuklash ===")
    
    # 1. Lesson 10 ni topish
    # Title normalizatsiya qilinib yoki ordering bo'yicha qidiriladi
    lesson10 = Lesson.objects.filter(title__icontains="10.").first()
    if not lesson10:
        # Agar titlesiz bo'lsa order bo'yicha olamiz
        lesson10 = Lesson.objects.filter(order=10).first()
        
    if not lesson10:
        print("[!] 10-dars topilmadi. Avval darslarni yuklang.")
        return

    print(f"Dars topildi: [{lesson10.id}] {lesson10.title}")
    
    # 2. Yangi topshiriqlar ro'yxati
    new_tasks = [
        {
            "title": "ValueError xatosini ushlash",
            "question": "Berilgan `matn = 'besh'` o'zgaruvchisini `int(matn)` orqali butun songa aylantirishga harakat qiling. Agar `ValueError` yuz bersa, ekranga 'Butun son emas' yozuvini chiqaring.",
            "starter_code": "matn = \"besh\"\ntry:\n    # bu yerga kod yozing\nexcept ValueError:\n    # bu yerga kod yozing",
            "expected_output": "Butun son emas",
            "ai_hints": "try ichida int(matn) funksiyasini chaqiring, except ValueError: bloki ostida esa print('Butun son emas') yozing.",
            "difficulty": "intermediate",
            "order": 2
        },
        {
            "title": "IndexError xatosini ushlash",
            "question": "Berilgan `sonlar = [10, 20]` ro'yxatidan 5-indeksdagi elementni chiqarishga harakat qiling (ya'ni `sonlar[5]`). Agar `IndexError` yuz bersa, ekranga 'Indeks xato' yozuvini chiqaring.",
            "starter_code": "sonlar = [10, 20]\ntry:\n    # bu yerga kod yozing\nexcept IndexError:\n    # bu yerga kod yozing",
            "expected_output": "Indeks xato",
            "ai_hints": "try ichida sonlar[5] elementini olishga harakat qiling, except IndexError: bloki ostida print('Indeks xato') deb yozing.",
            "difficulty": "intermediate",
            "order": 3
        }
    ]

    for t in new_tasks:
        task, created = Task.objects.get_or_create(
            lesson=lesson10,
            title=t["title"],
            defaults={
                "question": t["question"],
                "starter_code": t["starter_code"],
                "expected_output": t["expected_output"],
                "ai_hints": t["ai_hints"],
                "difficulty": t["difficulty"],
                "order": t["order"]
            }
        )
        if created:
            print(f"[OK] Topshiriq yaratildi: {t['title']}")
        else:
            print(f"[SKIP] Topshiriq allaqachon mavjud: {t['title']}")
            
            # Agar mavjud bo'lsa-yu xususiyatlari farq qilsa, ularni yangilaymiz
            task.question = t["question"]
            task.starter_code = t["starter_code"]
            task.expected_output = t["expected_output"]
            task.ai_hints = t["ai_hints"]
            task.difficulty = t["difficulty"]
            task.order = t["order"]
            task.save()
            print(f"[UPD] Topshiriq qiymatlari yangilandi: {t['title']}")

    print("\n--- Yakuniy topshiriqlar soni ---")
    all_tasks = Task.objects.filter(lesson=lesson10).order_by('order')
    for idx, t in enumerate(all_tasks, 1):
        print(f"  {idx}. [{t.id}] {t.title}")
    
    print("\n=== Muvaffaqiyatli yakunlandi! ===")

if __name__ == "__main__":
    seed_missing_tasks()
