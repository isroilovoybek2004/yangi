"""
AI Lesson Skeleton Generator
=============================
Gemini API yordamida yangi dars skeleti yaratadi va DB ga yozadi.

Ishlatilishi:
    python manage.py generate_skeleton --topic "Funksiyalar" --type theory --difficulty beginner
    python manage.py generate_skeleton --topic "Sikllar" --type video --difficulty intermediate --course-id 1
"""

import json
import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from courses.models import Course
from lessons.models import Lesson, Task, Quiz, QuizQuestion, QuizChoice


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)

PROMPT_TEMPLATE = """
Sen Python dasturlash platformasi uchun dars skeleti yaratuvchi assistantsan.
Berilgan mavzu bo'yicha quyidagi JSON formatda javob ber (faqat JSON, boshqa hech narsa yo'q):

{{
  "lesson_title": "Dars nomi (o'zbekcha, qisqa va aniq)",
  "summary": "Dars haqida 1-2 jumlali qisqa tavsif (o'zbekcha)",
  "content_outline": "<h2>Asosiy mavzu</h2><p>[Bu yerga kontent kiritiladi]</p><h3>Misol</h3><pre><code>[Kod misoli]</code></pre>",
  "tasks": [
    {{
      "title": "Topshiriq nomi",
      "question": "Topshiriq sharti (o'zbekcha)",
      "starter_code": "# Bu yerga boshlang'ich kod",
      "expected_output": "natija",
      "ai_hints": "Maslahat matni"
    }}
  ]
}}

Qoidalar:
- Mavzu: {topic}
- Dars turi: {lesson_type}
- Daraja: {difficulty}
- Aynan {task_count} ta Task yarat
- Barcha matnlar o'zbekcha bo'lsin
- content_outline faqat HTML skeleton (haqiqiy content keyin qo'shiladi)
- tasks natijasi oddiy va aniq bo'lsin
"""


class Command(BaseCommand):
    help = "Gemini AI yordamida dars skeleti yaratadi"

    def add_arguments(self, parser):
        parser.add_argument('--topic',      required=True,  help="Dars mavzusi (masalan: 'Funksiyalar')")
        parser.add_argument('--type',       default='theory',
                            choices=['theory', 'video', 'mixed'],
                            help="Dars turi (default: theory)")
        parser.add_argument('--difficulty', default='beginner',
                            choices=['beginner', 'intermediate', 'advanced'],
                            help="Daraja (default: beginner)")
        parser.add_argument('--course-id',  type=int, default=None,
                            help="Qaysi kursga qo'shish (default: birinchi kurs)")
        parser.add_argument('--tasks',      type=int, default=3,
                            help="Nechta Task yaratilsin (default: 3)")
        parser.add_argument('--yes', '-y',  action='store_true',
                            help="Tasdiqlashsiz DB ga yozish")

    def handle(self, *args, **options):
        topic       = options['topic']
        lesson_type = options['type']
        difficulty  = options['difficulty']
        task_count  = options['tasks']
        auto_yes    = options['yes']
        course_id   = options['course_id']

        # Kursni topish
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                raise CommandError(f"Kurs topilmadi: ID={course_id}")
        else:
            course = Course.objects.first()
            if not course:
                raise CommandError("Hech qanday kurs topilmadi. Avval kurs yarating.")

        self.stdout.write(f"\n🤖 Gemini API ga so'rov yuborilmoqda...")
        self.stdout.write(f"   Mavzu: {topic} | Tur: {lesson_type} | Daraja: {difficulty}\n")

        prompt = PROMPT_TEMPLATE.format(
            topic=topic,
            lesson_type=lesson_type,
            difficulty=difficulty,
            task_count=task_count,
        )

        # Gemini API so'rovi
        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            raise CommandError("settings.py da GEMINI_API_KEY topilmadi.")

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2000,
                "responseMimeType": "application/json",
            }
        }

        try:
            resp = requests.post(
                GEMINI_URL,
                params={"key": api_key},
                json=payload,
                timeout=60,
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            raise CommandError(f"Gemini API xatosi: {e}")

        # Javobni parse qilish
        try:
            raw_text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
            # JSON bo'lsa to'g'ir parse qiling
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
            data = json.loads(raw_text.strip())
        except (KeyError, json.JSONDecodeError) as e:
            raise CommandError(f"Javobni parse qilib bo'lmadi: {e}\nJavob: {resp.text[:500]}")

        # Preview ko'rsatish
        self.stdout.write(self.style.SUCCESS("\n✅ Gemini javobi:\n"))
        self.stdout.write(f"   📚 Dars nomi   : {data.get('lesson_title', '—')}")
        self.stdout.write(f"   📝 Tavsif      : {data.get('summary', '—')}")
        self.stdout.write(f"   💻 Topshiriqlar: {len(data.get('tasks', []))} ta\n")

        for i, t in enumerate(data.get('tasks', []), 1):
            self.stdout.write(f"      Task {i}: {t.get('title', '—')}")

        # Tasdiqlash
        if not auto_yes:
            confirm = input("\n📥 DB ga yozilsinmi? [y/N]: ").strip().lower()
            if confirm != 'y':
                self.stdout.write(self.style.WARNING("❌ Bekor qilindi."))
                return

        # DB ga yozish
        next_order = Lesson.objects.filter(course=course).count() + 1
        lesson = Lesson.objects.create(
            course=course,
            title=data.get('lesson_title', topic),
            summary=data.get('summary', ''),
            content=data.get('content_outline', ''),
            lesson_type=lesson_type,
            difficulty=difficulty,
            estimated_minutes=5,
            order=next_order,
            is_ai_generated=True,
        )
        self.stdout.write(f"\n✅ Dars yaratildi: [{lesson.id}] {lesson.title}")

        for i, t in enumerate(data.get('tasks', []), 1):
            Task.objects.create(
                lesson=lesson,
                title=t.get('title', f'Topshiriq {i}'),
                question=t.get('question', ''),
                starter_code=t.get('starter_code', ''),
                expected_output=t.get('expected_output', ''),
                ai_hints=t.get('ai_hints', ''),
                difficulty=difficulty,
                order=i,
            )
            self.stdout.write(f"   💻 Task qo'shildi: {t.get('title', f'Task {i}')}")

        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Muvaffaqiyat! Admin panelda tahrirlang: /admin/lessons/lesson/{lesson.id}/change/"
        ))
