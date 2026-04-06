"""
Bulk Skeleton Populate Script — HAQIQIY CONTENT BILAN
=====================================================
3 ta yangi darsni haqiqiy content bilan DB ga qo'shish.

Ishlatilishi:
    python tmp/populate_skeleton.py
"""

import os
import sys
import django
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import Course
from lessons.models import Lesson, Task, Quiz, QuizQuestion, QuizChoice

User = get_user_model()

# ─────────────────────────────────────────────────────────────
#  HAQIQIY KONTENT
# ─────────────────────────────────────────────────────────────

SKELETON_DATA = [
    {
        "course_title": "Python Dasturlash Asoslari (To'liq Kurs)",
        "lessons": [

            # ═══════════════════════════════════
            #  DARS 7: LUG'ATLAR (DICTIONARY)
            # ═══════════════════════════════════
            {
                "title": "7. Lug'atlar (Dictionary) bilan ishlash",
                "lesson_type": "theory",
                "difficulty": "intermediate",
                "estimated_minutes": 6,
                "summary": "Python dictionary — kalit:qiymat juftliklari, yaratish va asosiy metodlar.",
                "content": """
<h2>Lug'atlar (Dictionary) nima?</h2>

<p><strong>Dictionary</strong> — bu ma'lumotlarni <code>kalit: qiymat</code> juftliklari ko'rinishida saqlaydigan tuzilma. Ro'yxatda elementlarga raqam (indeks) bilan kirilsa, lug'atda — <strong>kalit</strong> orqali kiriladi.</p>

<p>Hayotiy misol: Telefon daftarchangiz — ism (kalit) → telefon raqam (qiymat).</p>

<h3>Yaratish</h3>
<pre><code>talaba = {
    "ism": "Ali",
    "yosh": 20,
    "kurs": 2
}
print(talaba)
</code></pre>

<p>Lug'at <strong>jingalak qavslar</strong> <code>{ }</code> ichida yoziladi. Har bir element <code>kalit: qiymat</code> formatida.</p>

<h3>Qiymatga kirish</h3>
<pre><code>print(talaba["ism"])     # Ali
print(talaba["yosh"])    # 20
</code></pre>

<h3>Yangi element qo'shish va o'zgartirish</h3>
<pre><code>talaba["fakultet"] = "IT"     # Yangi kalit qo'shish
talaba["yosh"] = 21            # Mavjud qiymatni o'zgartirish
print(talaba)
</code></pre>

<h3>Asosiy metodlar</h3>
<ul>
  <li><code>.keys()</code> — barcha kalitlarni qaytaradi</li>
  <li><code>.values()</code> — barcha qiymatlarni qaytaradi</li>
  <li><code>.items()</code> — kalit-qiymat juftliklarini qaytaradi</li>
  <li><code>.get(kalit, default)</code> — xavfsiz qiymat olish</li>
</ul>

<pre><code>print(talaba.keys())    # dict_keys(['ism', 'yosh', 'kurs', 'fakultet'])
print(talaba.values())  # dict_values(['Ali', 21, 2, 'IT'])
</code></pre>
""",
                "tasks": [
                    {
                        "title": "Dictionary yaratish",
                        "question": "meva nomli dictionary yarating: 'nom' kalitiga 'olma', 'rang' kalitiga 'qizil', 'narx' kalitiga 5000 qiymatlarini bering. So'ng print(meva) orqali chop eting.",
                        "starter_code": "# meva dictionary yarating\n\nprint(meva)",
                        "expected_output": "{'nom': 'olma', 'rang': 'qizil', 'narx': 5000}",
                        "ai_hints": "meva = {'nom': 'olma', 'rang': 'qizil', 'narx': 5000} ko'rinishida yozing.",
                        "difficulty": "intermediate",
                    },
                    {
                        "title": "Qiymatga kirish",
                        "question": "talaba = {'ism': 'Jasur', 'yosh': 19, 'ball': 85}. Shu lug'atdan faqat 'ism' kalitining qiymatini ekranga chiqaring.",
                        "starter_code": "talaba = {'ism': 'Jasur', 'yosh': 19, 'ball': 85}\n# ism ni chiqaring",
                        "expected_output": "Jasur",
                        "ai_hints": "print(talaba['ism']) deb yozing. Kalit qo'shtirnoq ichida bo'lishi shart.",
                        "difficulty": "intermediate",
                    },
                    {
                        "title": "Kalitlarni chiqarish",
                        "question": "info = {'shahar': 'Toshkent', 'davlat': 'Uzbekistan'}. Shu lug'atning barcha kalitlarini .keys() metodi orqali ekranga chiqaring.",
                        "starter_code": "info = {'shahar': 'Toshkent', 'davlat': 'Uzbekistan'}\n# kalitlarni chiqaring",
                        "expected_output": "dict_keys(['shahar', 'davlat'])",
                        "ai_hints": "print(info.keys()) deb yozing.",
                        "difficulty": "intermediate",
                    },
                    {
                        "title": "Element qo'shish",
                        "question": "D = {'a': 1, 'b': 2}. Unga 'c' kalitiga 3 qiymatini qo'shing va to'liq lug'atni chop eting.",
                        "starter_code": "D = {'a': 1, 'b': 2}\n# 'c': 3 qo'shing\nprint(D)",
                        "expected_output": "{'a': 1, 'b': 2, 'c': 3}",
                        "ai_hints": "D['c'] = 3 orqali yangi kalit-qiymat qo'shiladi.",
                        "difficulty": "intermediate",
                    },
                ],
                "quizzes": [
                    {
                        "title": "Dictionary asoslari testi",
                        "questions": [
                            {
                                "question_text": "Python da dictionary qanday qavslar ichida yoziladi?",
                                "question_type": "multiple_choice",
                                "explanation": "Dictionary jingalak qavslar { } ichida yoziladi. [] — ro'yxat uchun, () — tuple uchun.",
                                "choices": [
                                    {"text": "Kvadrat qavslar [ ]", "is_correct": False},
                                    {"text": "Jingalak qavslar { }", "is_correct": True},
                                    {"text": "Oddiy qavslar ( )", "is_correct": False},
                                    {"text": "Burchak qavslar < >", "is_correct": False},
                                ],
                            },
                            {
                                "question_text": "d = {'x': 10, 'y': 20}. d['x'] ning natijasi nima?",
                                "question_type": "code_output",
                                "explanation": "d['x'] — 'x' kalitiga mos qiymatni qaytaradi, ya'ni 10.",
                                "choices": [
                                    {"text": "x", "is_correct": False},
                                    {"text": "10", "is_correct": True},
                                    {"text": "20", "is_correct": False},
                                    {"text": "Xatolik chiqadi", "is_correct": False},
                                ],
                            },
                            {
                                "question_text": "Dictionary da kalitlar takrorlanishi mumkin.",
                                "question_type": "true_false",
                                "explanation": "Dictionary da har bir kalit yagona bo'lishi shart. Agar takr. kalit yozilsa, oxirgi qiymat saqlanadi.",
                                "choices": [
                                    {"text": "✅ To'g'ri", "is_correct": False},
                                    {"text": "❌ Noto'g'ri", "is_correct": True},
                                ],
                            },
                        ],
                    }
                ],
            },

            # ═══════════════════════════════════
            #  DARS 8: OOP GA KIRISH
            # ═══════════════════════════════════
            {
                "title": "8. Python da OOP ga kirish",
                "lesson_type": "mixed",
                "difficulty": "advanced",
                "estimated_minutes": 10,
                "summary": "Ob'ektga yo'naltirilgan dasturlash asoslari: class, object, __init__, method.",
                "video_url": "https://www.youtube.com/embed/pnWINBJ3-yA",
                "content": """
<h2>OOP nima?</h2>

<p><strong>OOP (Object-Oriented Programming)</strong> — bu dasturni ob'ektlar (narsalar) asosida tuzish usuli. Hayotda har bir narsa (mashina, talaba, telefon) o'ziga xos <em>xususiyatlari</em> va <em>harakatlari</em> ga ega. Dasturlashda ham xuddi shunday.</p>

<h3>Class va Object</h3>
<p><code>Class</code> — bu qolip (shablon). <code>Object</code> — bu shu qolipdan yaratilgan aniq narsa.</p>

<pre><code>class Talaba:
    def __init__(self, ism, yosh):
        self.ism = ism
        self.yosh = yosh

    def salomlash(self):
        print(f"Salom, men {self.ism}, yoshim {self.yosh}")

# Object yaratish
t1 = Talaba("Ali", 20)
t1.salomlash()
</code></pre>

<h3>__init__ nima?</h3>
<p><code>__init__</code> — bu maxsus metod (konstruktor). Object yaratilganda avtomatik ishga tushadi va boshlang'ich qiymatlarni o'rnatadi.</p>

<h3>self nima?</h3>
<p><code>self</code> — bu ob'ektning o'ziga ishora. Har bir metodda birinchi parametr sifatida yoziladi.</p>

<pre><code>class Hisob:
    def __init__(self, balans):
        self.balans = balans

    def tekshir(self):
        print(f"Balans: {self.balans} so'm")

h = Hisob(50000)
h.tekshir()
</code></pre>
""",
                "tasks": [
                    {
                        "title": "Class yaratish",
                        "question": "Mashina nomli class yarating. __init__ da 'nomi' va 'rangi' parametrlarini qabul qilsin. info() metodi 'Mashina: [nomi], Rangi: [rangi]' deb chop etsin. m = Mashina('Cobalt', 'oq') yaratib m.info() ni chaqiring.",
                        "starter_code": "class Mashina:\n    # __init__ va info() yozing\n    pass\n\nm = Mashina('Cobalt', 'oq')\nm.info()",
                        "expected_output": "Mashina: Cobalt, Rangi: oq",
                        "ai_hints": "def __init__(self, nomi, rangi): self.nomi = nomi ... def info(self): print(f'Mashina: {self.nomi}, Rangi: {self.rangi}')",
                        "difficulty": "advanced",
                    },
                    {
                        "title": "Metodlar bilan ishlash",
                        "question": "Hisoblagich class yarating. __init__ da self.son = 0 bo'lsin. oshir() metodi self.son ni 1 ga oshirsin. korsat() metodi self.son ni chop etsin. h = Hisoblagich() yaratib, 3 marta h.oshir() chaqiring, keyin h.korsat() ni chaqiring.",
                        "starter_code": "class Hisoblagich:\n    pass\n\nh = Hisoblagich()\nh.oshir()\nh.oshir()\nh.oshir()\nh.korsat()",
                        "expected_output": "3",
                        "ai_hints": "def oshir(self): self.son += 1 va def korsat(self): print(self.son)",
                        "difficulty": "advanced",
                    },
                    {
                        "title": "Ob'ekt xususiyatlarini chiqarish",
                        "question": "Kitob classini yarating: __init__ da nom va sahifa (int) qabul qilsin. k = Kitob('Python', 350) yaratib, print(k.sahifa) chiqaring.",
                        "starter_code": "class Kitob:\n    pass\n\nk = Kitob('Python', 350)\nprint(k.sahifa)",
                        "expected_output": "350",
                        "ai_hints": "def __init__(self, nom, sahifa): self.nom = nom; self.sahifa = sahifa",
                        "difficulty": "advanced",
                    },
                ],
                "quizzes": [
                    {
                        "title": "OOP asoslari testi",
                        "questions": [
                            {
                                "question_text": "__init__ metodi qachon ishga tushadi?",
                                "question_type": "multiple_choice",
                                "explanation": "__init__ ob'ekt yaratilganda (masalan, t = Talaba()) avtomatik chaqiriladi.",
                                "choices": [
                                    {"text": "Dastur tugaganda", "is_correct": False},
                                    {"text": "Ob'ekt yaratilganda", "is_correct": True},
                                    {"text": "Faqat chaqirilganda", "is_correct": False},
                                    {"text": "Hech qachon", "is_correct": False},
                                ],
                            },
                            {
                                "question_text": "self — bu classning o'ziga ishora qiladi.",
                                "question_type": "true_false",
                                "explanation": "self ob'ektning o'ziga ishora qiladi (classga emas), shu ob'ektning xususiyatlariga kirish uchun ishlatiladi.",
                                "choices": [
                                    {"text": "✅ To'g'ri", "is_correct": False},
                                    {"text": "❌ Noto'g'ri", "is_correct": True},
                                ],
                            },
                        ],
                    }
                ],
            },

            # ═══════════════════════════════════
            #  DARS 9: MODULLAR VA PAKETLAR
            # ═══════════════════════════════════
            {
                "title": "9. Modullar va paketlar",
                "lesson_type": "theory",
                "difficulty": "intermediate",
                "estimated_minutes": 7,
                "summary": "Python da import, standart kutubxona va tashqi paketlardan foydalanish.",
                "content": """
<h2>Modullar (Modules)</h2>

<p>Python da tayyor yozilgan kodlar to'plami <strong>modul</strong> deb ataladi. Ularni <code>import</code> qilib o'z dasturingizda ishlatishingiz mumkin. Bu g'ildirakni qayta ixtiro qilmaslik uchun!</p>

<h3>Import qilish usullari</h3>
<pre><code># To'liq import
import math
print(math.pi)        # 3.141592653589793
print(math.sqrt(16))  # 4.0

# Aniq funktsiyani import
from math import factorial
print(factorial(5))   # 120

# Taxallus (alias) bilan
import random as r
print(r.randint(1, 10))  # 1 dan 10 gacha tasodifiy son
</code></pre>

<h3>Eng ko'p ishlatiladigan modullar</h3>
<ul>
  <li><code>math</code> — matematik funksiyalar (pi, sqrt, factorial)</li>
  <li><code>random</code> — tasodifiy sonlar va tanlash</li>
  <li><code>datetime</code> — sana va vaqt bilan ishlash</li>
  <li><code>os</code> — operatsion tizim bilan aloqa</li>
  <li><code>json</code> — JSON formatda ma'lumot bilan ishlash</li>
</ul>

<h3>random moduli</h3>
<pre><code>import random

# Tasodifiy butun son
print(random.randint(1, 100))

# Ro'yxatdan tasodifiy tanlash
ranglar = ["qizil", "yashil", "ko'k"]
print(random.choice(ranglar))
</code></pre>

<h3>datetime moduli</h3>
<pre><code>from datetime import datetime

hozir = datetime.now()
print(hozir.year)   # Joriy yil
print(hozir.month)  # Joriy oy
</code></pre>
""",
                "tasks": [
                    {
                        "title": "math modulidan foydalanish",
                        "question": "math modulini import qiling va math.sqrt(144) natijasini ekranga chiqaring.",
                        "starter_code": "# math ni import qiling\n# sqrt(144) ni chop eting",
                        "expected_output": "12.0",
                        "ai_hints": "import math deb yozing, keyin print(math.sqrt(144))",
                        "difficulty": "intermediate",
                    },
                    {
                        "title": "factorial hisoblash",
                        "question": "math modulidan factorial funksiyasini import qiling va factorial(6) natijasini chop eting. (6! = 720)",
                        "starter_code": "# from math import factorial\n# factorial(6) ni chop eting",
                        "expected_output": "720",
                        "ai_hints": "from math import factorial va print(factorial(6))",
                        "difficulty": "intermediate",
                    },
                    {
                        "title": "pi sonini chiqarish",
                        "question": "math modulidan pi konstantasini import qilib, uni ekranga chiqaring.",
                        "starter_code": "# pi ni import qiling va chop eting",
                        "expected_output": "3.141592653589793",
                        "ai_hints": "from math import pi va print(pi) yoki import math va print(math.pi)",
                        "difficulty": "intermediate",
                    },
                ],
                "quizzes": [
                    {
                        "title": "Modullar testi",
                        "questions": [
                            {
                                "question_text": "Quyidagi kodning natijasi nima?\n\nimport math\nprint(math.sqrt(25))",
                                "question_type": "code_output",
                                "explanation": "math.sqrt(25) — 25 ning kvadrat ildizini hisoblaydi, natija 5.0 (float).",
                                "choices": [
                                    {"text": "5", "is_correct": False},
                                    {"text": "5.0", "is_correct": True},
                                    {"text": "25", "is_correct": False},
                                    {"text": "Xatolik", "is_correct": False},
                                ],
                            },
                            {
                                "question_text": "from math import pi — bu qanday import turi?",
                                "question_type": "multiple_choice",
                                "explanation": "from ... import ... — bu aniq (specific) import, faqat kerakli funksiya/konstantani olib keladi.",
                                "choices": [
                                    {"text": "To'liq import", "is_correct": False},
                                    {"text": "Aniq (specific) import", "is_correct": True},
                                    {"text": "Yulduzcha import", "is_correct": False},
                                    {"text": "Shartli import", "is_correct": False},
                                ],
                            },
                            {
                                "question_text": "random.randint(1, 10) har doim 10 ni qaytaradi.",
                                "question_type": "true_false",
                                "explanation": "random.randint(1, 10) 1 dan 10 gacha tasodifiy son qaytaradi, har doim 10 emas.",
                                "choices": [
                                    {"text": "✅ To'g'ri", "is_correct": False},
                                    {"text": "❌ Noto'g'ri", "is_correct": True},
                                ],
                            },
                        ],
                    }
                ],
            },

        ]
    },
]


# ─────────────────────────────────────────────────────────────

def populate(course_id=None, clear=False):
    for course_data in SKELETON_DATA:
        course_title = course_data['course_title']

        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                print(f"❌ Kurs topilmadi: ID={course_id}")
                return
        else:
            course = Course.objects.filter(title=course_title).first()
            if not course:
                print(f"❌ Kurs topilmadi: '{course_title}'")
                continue

        print(f"\n📚 Kurs: {course.title}")

        if clear:
            deleted = Lesson.objects.filter(course=course).delete()
            print(f"   🗑  {deleted[0]} ta dars o'chirildi")

        for l_data in course_data['lessons']:
            existing = Lesson.objects.filter(course=course, title=l_data['title']).first()
            if existing:
                print(f"   ⚠️  Mavjud (o'tkazildi): {l_data['title']}")
                continue

            next_order = Lesson.objects.filter(course=course).count() + 1

            lesson = Lesson.objects.create(
                course=course,
                title=l_data['title'],
                summary=l_data.get('summary', ''),
                content=l_data.get('content', ''),
                lesson_type=l_data.get('lesson_type', 'theory'),
                difficulty=l_data.get('difficulty', 'beginner'),
                estimated_minutes=l_data.get('estimated_minutes', 5),
                video_url=l_data.get('video_url', '') or '',
                order=next_order,
            )
            print(f"\n   ✅ Dars qo'shildi: [{lesson.id}] {lesson.title}")

            for idx, t in enumerate(l_data.get('tasks', []), 1):
                Task.objects.create(
                    lesson=lesson,
                    title=t.get('title', f'Topshiriq {idx}'),
                    question=t.get('question', ''),
                    starter_code=t.get('starter_code', ''),
                    expected_output=t.get('expected_output', ''),
                    ai_hints=t.get('ai_hints', ''),
                    difficulty=t.get('difficulty', lesson.difficulty),
                    order=idx,
                )
                print(f"      💻 Task: {t.get('title')}")

            for q_idx, quiz_data in enumerate(l_data.get('quizzes', []), 1):
                quiz = Quiz.objects.create(
                    lesson=lesson,
                    title=quiz_data.get('title', f'Test {q_idx}'),
                    order=q_idx,
                )
                print(f"      📝 Quiz: {quiz.title}")

                for s_idx, q in enumerate(quiz_data.get('questions', []), 1):
                    question = QuizQuestion.objects.create(
                        quiz=quiz,
                        question_text=q.get('question_text', f'Savol {s_idx}'),
                        question_type=q.get('question_type', 'multiple_choice'),
                        explanation=q.get('explanation', ''),
                        order=s_idx,
                    )
                    for c in q.get('choices', []):
                        QuizChoice.objects.create(
                            question=question,
                            choice_text=c.get('text', ''),
                            is_correct=c.get('is_correct', False),
                        )
                    print(f"         ❓ Savol {s_idx}: {q.get('question_text', '')[:50]}...")

    print("\n" + "=" * 50)
    print("✅ populate_skeleton.py muvaffaqiyatli yakunlandi!")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Darslarni DB ga qo'shish")
    parser.add_argument('--course-id', type=int, default=None)
    parser.add_argument('--clear', action='store_true')
    args = parser.parse_args()

    if args.clear:
        confirm = input("⚠️  Mavjud darslar o'chiriladimi? [y/N]: ").strip().lower()
        if confirm != 'y':
            print("Bekor qilindi.")
            return

    populate(course_id=args.course_id, clear=args.clear)


if __name__ == "__main__":
    main()
