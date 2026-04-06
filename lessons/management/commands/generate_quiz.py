"""
AI Quiz Savol Generator
=========================
Gemini API yordamida test savollari va javob variantlarini yaratadi.

Ishlatilishi:
    python manage.py generate_quiz --lesson-id 3 --count 5
    python manage.py generate_quiz --topic "Python ro'yxatlar" --type multiple_choice --count 3
    python manage.py generate_quiz --topic "if-else" --type true_false --count 4
    python manage.py generate_quiz --topic "for sikli" --type code_output --count 3
"""

import json
import requests
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from lessons.models import Lesson, Quiz, QuizQuestion, QuizChoice


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)

PROMPTS = {
    "multiple_choice": """
Sen Python dasturlash bo'yicha test savollari yaratuvchi assistantsan.
Berilgan mavzu uchun {count} ta "Ko'p tanlov" (A/B/C/D) savoli yarat.
Faqat JSON formatda javob ber:

{{
  "quiz_title": "Test nomi (o'zbekcha)",
  "questions": [
    {{
      "question_text": "Savol matni (o'zbekcha)",
      "explanation": "To'g'ri javob tushuntirishi",
      "choices": [
        {{"text": "A variant", "is_correct": false}},
        {{"text": "B variant (to'g'ri javob)", "is_correct": true}},
        {{"text": "C variant", "is_correct": false}},
        {{"text": "D variant", "is_correct": false}}
      ]
    }}
  ]
}}

Mavzu: {topic}
Qoidalar: barcha matnlar o'zbekcha, har savolda aynan 1 ta to'g'ri javob, savol Python kodiga oid bo'lsin.
""",

    "true_false": """
Sen Python dasturlash bo'yicha test savollari yaratuvchi assistantsan.
Berilgan mavzu uchun {count} ta "To'g'ri/Noto'g'ri" savoli yarat.
Faqat JSON formatda javob ber:

{{
  "quiz_title": "Test nomi (o'zbekcha)",
  "questions": [
    {{
      "question_text": "Savol bayonoti (to'g'ri yoki noto'g'ri aniqlansa bo'ladigan)",
      "explanation": "Nima uchun to'g'ri yoki noto'g'ri ekanligi",
      "choices": [
        {{"text": "✅ To'g'ri", "is_correct": true}},
        {{"text": "❌ Noto'g'ri", "is_correct": false}}
      ]
    }}
  ]
}}

Mavzu: {topic}
Qoidalar: barcha matnlar o'zbekcha, choices listida is_correct qiymatlaridan faqat bittasi true, ba'zi savollar noto'g'ri bayonot bo'lsin.
""",

    "code_output": """
Sen Python dasturlash bo'yicha test savollari yaratuvchi assistantsan.
Berilgan mavzu uchun {count} ta "Kod natijasini toping" savoli yarat.
Faqat JSON formatda javob ber:

{{
  "quiz_title": "Test nomi (o'zbekcha)",
  "questions": [
    {{
      "question_text": "Quyidagi kod qanday natija beradi?\\n\\n```python\\n[Python kodi]\\n```",
      "explanation": "Kodni tahlil: nima uchun shu natija chiqadi",
      "choices": [
        {{"text": "Variant 1", "is_correct": false}},
        {{"text": "To'g'ri natija", "is_correct": true}},
        {{"text": "Variant 3", "is_correct": false}},
        {{"text": "Variant 4", "is_correct": false}}
      ]
    }}
  ]
}}

Mavzu: {topic}
Qoidalar: kod qisqa (3-5 qator), natijalar aniq va farqli bo'lsin, o'quvchi tushunishi uchun qiyin ammo adolatli.
"""
}


class Command(BaseCommand):
    help = "Gemini AI yordamida quiz savollari yaratadi"

    def add_arguments(self, parser):
        parser.add_argument('--topic',     default=None,
                            help="Savol mavzusi (masalan: 'Python ro\\'yxatlar')")
        parser.add_argument('--lesson-id', dest='lesson_id', type=int, default=None,
                            help="Qaysi lesson uchun (ID). lesson topilsa topic avtomatik olinadi")
        parser.add_argument('--type',      default='multiple_choice',
                            choices=['multiple_choice', 'true_false', 'code_output'],
                            dest='question_type',
                            help="Savol turi (default: multiple_choice)")
        parser.add_argument('--count',     type=int, default=4,
                            help="Nechta savol yaratilsin (default: 4)")
        parser.add_argument('--yes', '-y', action='store_true',
                            help="Tasdiqlashsiz DB ga yozish")

    def handle(self, *args, **options):
        topic         = options['topic']
        lesson_id     = options['lesson_id']
        question_type = options['question_type']
        count         = options['count']
        auto_yes      = options['yes']

        # Lesson topish
        lesson = None
        if lesson_id:
            try:
                lesson = Lesson.objects.get(id=lesson_id)
                if not topic:
                    topic = lesson.title
            except Lesson.DoesNotExist:
                raise CommandError(f"Lesson topilmadi: ID={lesson_id}")

        if not topic:
            raise CommandError("--topic yoki --lesson-id ko'rsatish shart.")

        type_labels = {
            'multiple_choice': "Ko'p tanlov",
            'true_false':      "To'g'ri/Noto'g'ri",
            'code_output':     "Kod natijasini toping",
        }
        self.stdout.write(
            f"\n🤖 Gemini API: '{topic}' mavzusi bo'yicha "
            f"{count} ta '{type_labels[question_type]}' savoli yaratilmoqda...\n"
        )

        # Prompt tayyorlash
        prompt = PROMPTS[question_type].format(topic=topic, count=count)

        api_key = getattr(settings, 'GEMINI_API_KEY', None)
        if not api_key:
            raise CommandError("settings.py da GEMINI_API_KEY topilmadi.")

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.8,
                "maxOutputTokens": 3000,
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
            if raw_text.startswith("```"):
                raw_text = raw_text.split("```")[1]
                if raw_text.startswith("json"):
                    raw_text = raw_text[4:]
            data = json.loads(raw_text.strip())
        except (KeyError, json.JSONDecodeError) as e:
            raise CommandError(f"Javobni parse qilib bo'lmadi: {e}\nJavob: {resp.text[:500]}")

        # Preview
        quiz_title = data.get('quiz_title', f"{topic} — Test")
        questions  = data.get('questions', [])

        self.stdout.write(self.style.SUCCESS(f"\n✅ Gemini javobi:\n"))
        self.stdout.write(f"   📝 Test nomi : {quiz_title}")
        self.stdout.write(f"   ❓ Savollar  : {len(questions)} ta\n")

        for i, q in enumerate(questions, 1):
            self.stdout.write(f"\n   Savol {i}: {q.get('question_text', '')[:80]}...")
            for c in q.get('choices', []):
                mark = "✅" if c.get('is_correct') else "  "
                self.stdout.write(f"      {mark} {c.get('text', '')}")

        # Tasdiqlash
        if not auto_yes:
            confirm = input("\n📥 DB ga yozilsinmi? [y/N]: ").strip().lower()
            if confirm != 'y':
                self.stdout.write(self.style.WARNING("❌ Bekor qilindi."))
                return

        # Lesson bo'lmasa birinchisini olish
        if not lesson:
            lesson = Lesson.objects.first()
            if not lesson:
                raise CommandError("Hech qanday dars topilmadi. Avval dars yarating.")
            self.stdout.write(
                self.style.WARNING(f"⚠️  --lesson-id ko'rsatilmagan. Birinchi darsga qo'shildi: '{lesson.title}'")
            )

        # DB ga yozish
        next_order = Quiz.objects.filter(lesson=lesson).count() + 1
        quiz = Quiz.objects.create(
            lesson=lesson,
            title=quiz_title,
            order=next_order,
        )
        self.stdout.write(f"\n✅ Quiz yaratildi: [{quiz.id}] {quiz.title}")

        for i, q in enumerate(questions, 1):
            question = QuizQuestion.objects.create(
                quiz=quiz,
                question_text=q.get('question_text', f'Savol {i}'),
                question_type=question_type,
                explanation=q.get('explanation', ''),
                order=i,
            )
            for c in q.get('choices', []):
                QuizChoice.objects.create(
                    question=question,
                    choice_text=c.get('text', ''),
                    is_correct=c.get('is_correct', False),
                )
            self.stdout.write(f"   ❓ Savol qo'shildi: {q.get('question_text', '')[:60]}...")

        self.stdout.write(self.style.SUCCESS(
            f"\n🎉 Muvaffaqiyat! Admin panelda ko'rish: /admin/lessons/quiz/{quiz.id}/change/"
        ))
