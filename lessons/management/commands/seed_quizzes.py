"""
Seed Quizzes — Nazariy Savol-Javoblar
=======================================
Har bir dars uchun kamida 5 ta test savoli (ko'p tanlov) qo'shadi.
Bu savollar rahbar maslahatiga ko'ra qo'shilgan nazariy savol-javoblar.

Ishlatilishi:
    python manage.py seed_quizzes
    python manage.py seed_quizzes --lesson-id 20
    python manage.py seed_quizzes --force   (mavjudlarini o'chirib qayta yozadi)
"""

from django.core.management.base import BaseCommand
from lessons.models import Lesson, Quiz, QuizQuestion, QuizChoice


# ─────────────────────────────────────────────────────────────
#  BARCHA DARSLAR UCHUN TESTLAR
# ─────────────────────────────────────────────────────────────

QUIZZES_DATA = {

    # ── Dars 1: Kirish va Python haqida tushuncha ──────────────
    "1. Kirish va Python haqida tushuncha": {
        "quiz_title": "Python asoslari — nazariy test",
        "questions": [
            {
                "question_text": "Python qaysi yilda yaratilgan va kim tomonidan ishlab chiqilgan?",
                "explanation": "Python 1991-yilda Guido van Rossum tomonidan yaratilgan.",
                "choices": [
                    {"text": "1985-yil, Dennis Ritchie", "is_correct": False},
                    {"text": "1991-yil, Guido van Rossum", "is_correct": True},
                    {"text": "2000-yil, Linus Torvalds", "is_correct": False},
                    {"text": "1995-yil, James Gosling", "is_correct": False},
                ]
            },
            {
                "question_text": "Python qaysi turdagi dasturlash tili hisoblanadi?",
                "explanation": "Python — interpretatsiya qilinadigan (interpreted), yuqori darajali (high-level), umumiy maqsadli dasturlash tilidir.",
                "choices": [
                    {"text": "Compiled (kompilyatsiya qilinadigan) til", "is_correct": False},
                    {"text": "Assembly tili", "is_correct": False},
                    {"text": "Interpreted (interpretatsiya qilinadigan) yuqori darajali til", "is_correct": True},
                    {"text": "Faqat web uchun mo'ljallangan til", "is_correct": False},
                ]
            },
            {
                "question_text": "Python da birinchi dasturni chop etish uchun qaysi funksiya ishlatiladi?",
                "explanation": "print() funksiyasi ekranga matn yoki qiymatlarni chiqarish uchun ishlatiladi.",
                "choices": [
                    {"text": "echo()", "is_correct": False},
                    {"text": "write()", "is_correct": False},
                    {"text": "console.log()", "is_correct": False},
                    {"text": "print()", "is_correct": True},
                ]
            },
            {
                "question_text": "Python da izoh (comment) yozish uchun qaysi belgi ishlatiladi?",
                "explanation": "# belgisi Python da bir qatorli izoh yozish uchun ishlatiladi.",
                "choices": [
                    {"text": "// (ikki slash)", "is_correct": False},
                    {"text": "/* */ (ko'p qatorli)", "is_correct": False},
                    {"text": "# (panjara belgisi)", "is_correct": True},
                    {"text": "-- (ikki chiziq)", "is_correct": False},
                ]
            },
            {
                "question_text": "Python versiyasini terminalda tekshirish uchun qaysi buyruq ishlatiladi?",
                "explanation": "python --version yoki python3 --version buyrug'i o'rnatilgan Python versiyasini ko'rsatadi.",
                "choices": [
                    {"text": "python -info", "is_correct": False},
                    {"text": "python --version", "is_correct": True},
                    {"text": "python -check", "is_correct": False},
                    {"text": "version python", "is_correct": False},
                ]
            },
            {
                "question_text": "Quyidagi Python kodi qanday natija beradi?\n\nprint(2 + 3 * 4)",
                "explanation": "Matematika qoidalariga ko'ra avval ko'paytma bajariladi: 3*4=12, keyin 2+12=14.",
                "choices": [
                    {"text": "20", "is_correct": False},
                    {"text": "14", "is_correct": True},
                    {"text": "24", "is_correct": False},
                    {"text": "Xato (error)", "is_correct": False},
                ]
            },
        ]
    },

    # ── Dars 2: O'zgaruvchilar va ma'lumot turlari ─────────────
    "2. O'zgaruvchilar va ma'lumot turlari": {
        "quiz_title": "O'zgaruvchilar va ma'lumot turlari — nazariy test",
        "questions": [
            {
                "question_text": "Python da o'zgaruvchini e'lon qilish uchun qaysi kalit so'z ishlatiladi?",
                "explanation": "Python da o'zgaruvchilarni e'lon qilish uchun maxsus kalit so'z kerak emas, shunchaki nom = qiymat yoziladi.",
                "choices": [
                    {"text": "var nom = 5", "is_correct": False},
                    {"text": "int nom = 5", "is_correct": False},
                    {"text": "nom = 5 (kalit so'zsiz)", "is_correct": True},
                    {"text": "let nom = 5", "is_correct": False},
                ]
            },
            {
                "question_text": "type(3.14) qanday natija qaytaradi?",
                "explanation": "3.14 — bu float (haqiqiy son) turi, shuning uchun <class 'float'> qaytariladi.",
                "choices": [
                    {"text": "<class 'int'>", "is_correct": False},
                    {"text": "<class 'str'>", "is_correct": False},
                    {"text": "<class 'float'>", "is_correct": True},
                    {"text": "<class 'number'>", "is_correct": False},
                ]
            },
            {
                "question_text": "Quyidagi o'zgaruvchilar nomlaridan qaysi biri noto'g'ri?",
                "explanation": "Python da o'zgaruvchi nomi raqamdan boshlanishi mumkin emas. 3mening_nom noto'g'ri.",
                "choices": [
                    {"text": "mening_nom", "is_correct": False},
                    {"text": "_maxfiy", "is_correct": False},
                    {"text": "3mening_nom", "is_correct": True},
                    {"text": "nom2", "is_correct": False},
                ]
            },
            {
                "question_text": "Python da butun son va matni bir xil o'zgaruvchiga birlashtirish uchun nima qilish kerak?",
                "explanation": "str() funksiyasi yordamida butun son matnga o'giriladi, keyin + operatori bilan birlashtiriladi.",
                "choices": [
                    {"text": "print(5 + 'yosh') — to'g'ridan to'g'ri", "is_correct": False},
                    {"text": "print(str(5) + 'yosh') — str() orqali o'girish", "is_correct": True},
                    {"text": "print(int('yosh') + 5)", "is_correct": False},
                    {"text": "Python avtomatik birlashtiradi", "is_correct": False},
                ]
            },
            {
                "question_text": "Boolean ma'lumot turining qiymatlari qaysilar?",
                "explanation": "Python da Boolean turi faqat True yoki False qiymatlarini qabul qiladi (bosh harf bilan yoziladi).",
                "choices": [
                    {"text": "1 va 0", "is_correct": False},
                    {"text": "true va false (kichik harf)", "is_correct": False},
                    {"text": "True va False (bosh harf)", "is_correct": True},
                    {"text": "yes va no", "is_correct": False},
                ]
            },
            {
                "question_text": "x = '5' va y = 5 o'zgaruvchilarida x == y ifodasi qanday natija beradi?",
                "explanation": "x matn ('5'), y esa butun son (5). Python da == operatori tur va qiymatni birga tekshiradi, shuning uchun False.",
                "choices": [
                    {"text": "True", "is_correct": False},
                    {"text": "False", "is_correct": True},
                    {"text": "Xato (TypeError)", "is_correct": False},
                    {"text": "None", "is_correct": False},
                ]
            },
        ]
    },

    # ── Dars 3: Shartli operatorlar ────────────────────────────
    "3. Shartli operatorlar (if, elif, else)": {
        "quiz_title": "Shartli operatorlar — nazariy test",
        "questions": [
            {
                "question_text": "Python da if bloki qanday yoziladi?",
                "explanation": "if shart: ko'rinishida yoziladi, ikki nuqta (:) majburiy, keyin ichki blok bo'sh joy (indentation) bilan yoziladi.",
                "choices": [
                    {"text": "if (shart) { }", "is_correct": False},
                    {"text": "if shart:", "is_correct": True},
                    {"text": "IF shart THEN", "is_correct": False},
                    {"text": "if shart end", "is_correct": False},
                ]
            },
            {
                "question_text": "elif kalit so'zi nimani bildiradi?",
                "explanation": "elif — 'else if' ning qisqartmasi bo'lib, birinchi shart noto'g'ri bo'lsa keyingi shartni tekshiradi.",
                "choices": [
                    {"text": "Dastlab bajariluvchi blok", "is_correct": False},
                    {"text": "Doim bajariladigan blok", "is_correct": False},
                    {"text": "Birinchi shart noto'g'ri bo'lsa tekshiriladigan qo'shimcha shart", "is_correct": True},
                    {"text": "Siklni to'xtatuvchi operator", "is_correct": False},
                ]
            },
            {
                "question_text": "Quyidagi kod qanday natija chiqaradi?\n\nx = 10\nif x > 5:\n    print('Katta')\nelse:\n    print('Kichik')",
                "explanation": "x = 10 > 5 sharti rost, shuning uchun 'Katta' chiqadi.",
                "choices": [
                    {"text": "Kichik", "is_correct": False},
                    {"text": "Katta", "is_correct": True},
                    {"text": "Xato", "is_correct": False},
                    {"text": "Hech narsa chiqmaydi", "is_correct": False},
                ]
            },
            {
                "question_text": "Python da mantiqiy 'VA' operatori qanday yoziladi?",
                "explanation": "Python da VA operatori 'and' kalit so'zi orqali yoziladi (&&  emas).",
                "choices": [
                    {"text": "&&", "is_correct": False},
                    {"text": "AND", "is_correct": False},
                    {"text": "and", "is_correct": True},
                    {"text": "&", "is_correct": False},
                ]
            },
            {
                "question_text": "Quyidagi shartlardan qaysi biri True qaytaradi?\n\nx = 7",
                "explanation": "7 > 5 sharti rost va 7 < 10 sharti rost, ikkalasi and bilan True beradi.",
                "choices": [
                    {"text": "x > 10", "is_correct": False},
                    {"text": "x == 8", "is_correct": False},
                    {"text": "x > 5 and x < 10", "is_correct": True},
                    {"text": "x < 5 or x > 20", "is_correct": False},
                ]
            },
            {
                "question_text": "not True ifodasi qanday qiymat qaytaradi?",
                "explanation": "not operatori mantiqiy qiymatni teskarisiga aylantiradi: not True = False.",
                "choices": [
                    {"text": "True", "is_correct": False},
                    {"text": "False", "is_correct": True},
                    {"text": "None", "is_correct": False},
                    {"text": "Xato", "is_correct": False},
                ]
            },
        ]
    },

    # ── Dars 4: Sikllar ────────────────────────────────────────
    "4. Sikllar (for va while)": {
        "quiz_title": "Sikllar — nazariy test",
        "questions": [
            {
                "question_text": "range(5) funksiyasi qanday qiymatlar qaytaradi?",
                "explanation": "range(5) — 0 dan 4 gacha (5 kiritilmaydi) bo'lgan qiymatlarni qaytaradi: 0, 1, 2, 3, 4.",
                "choices": [
                    {"text": "1, 2, 3, 4, 5", "is_correct": False},
                    {"text": "0, 1, 2, 3, 4", "is_correct": True},
                    {"text": "0, 1, 2, 3, 4, 5", "is_correct": False},
                    {"text": "1, 2, 3, 4", "is_correct": False},
                ]
            },
            {
                "question_text": "while sikli qachon bajarilishni to'xtatadi?",
                "explanation": "while sikli sharti False bo'lganda to'xtaydi. Agar shart doim True bo'lsa, cheksiz sikl hosil bo'ladi.",
                "choices": [
                    {"text": "Faqat break buyrug'i bilan", "is_correct": False},
                    {"text": "Shart False bo'lganda yoki break chaqirilganda", "is_correct": True},
                    {"text": "10 marta bajarilgandan so'ng", "is_correct": False},
                    {"text": "Hech qachon to'xtamaydi", "is_correct": False},
                ]
            },
            {
                "question_text": "Quyidagi for siklida nechta marta 'Salom' chiqadi?\n\nfor i in range(3):\n    print('Salom')",
                "explanation": "range(3) — 0, 1, 2 uchta qiymat beradi, shuning uchun 'Salom' 3 marta chiqadi.",
                "choices": [
                    {"text": "2 marta", "is_correct": False},
                    {"text": "3 marta", "is_correct": True},
                    {"text": "4 marta", "is_correct": False},
                    {"text": "Bajarilmaydi", "is_correct": False},
                ]
            },
            {
                "question_text": "break buyrug'i nima qiladi?",
                "explanation": "break — joriy siklni to'liq to'xtatadi va sikldan chiqadi.",
                "choices": [
                    {"text": "Joriy iteratsiyani o'tkazib yuboradi", "is_correct": False},
                    {"text": "Dasturni to'liq to'xtatadi", "is_correct": False},
                    {"text": "Joriy siklni to'liq to'xtatadi", "is_correct": True},
                    {"text": "Siklni boshidan qayta boshlaydi", "is_correct": False},
                ]
            },
            {
                "question_text": "continue buyrug'i nima qiladi?",
                "explanation": "continue — joriy iteratsiyaning qolgan qismini o'tkazib yuborib, keyingi iteratsiyaga o'tadi.",
                "choices": [
                    {"text": "Siklni to'xtatadi", "is_correct": False},
                    {"text": "Joriy iteratsiyani o'tkazib keyingisiga o'tadi", "is_correct": True},
                    {"text": "Dastur oxiriga o'tadi", "is_correct": False},
                    {"text": "Sikl boshiga qaytadi va hisoblagichni 0 qiladi", "is_correct": False},
                ]
            },
            {
                "question_text": "range(2, 10, 2) qanday qiymatlar beradi?",
                "explanation": "range(start, stop, step) — 2 dan boshlab, 10 gacha (kiritilmaydi), 2 qadam bilan: 2, 4, 6, 8.",
                "choices": [
                    {"text": "2, 4, 6, 8, 10", "is_correct": False},
                    {"text": "2, 4, 6, 8", "is_correct": True},
                    {"text": "0, 2, 4, 6, 8", "is_correct": False},
                    {"text": "2, 3, 4, 5, 6, 7, 8, 9", "is_correct": False},
                ]
            },
        ]
    },

    # ── Dars 5: Funksiyalar ────────────────────────────────────
    "5. Funksiyalar bilan ishlash": {
        "quiz_title": "Funksiyalar — nazariy test",
        "questions": [
            {
                "question_text": "Python da funksiya e'lon qilish uchun qaysi kalit so'z ishlatiladi?",
                "explanation": "def kalit so'zi funksiyani aniqlash (define) uchun ishlatiladi.",
                "choices": [
                    {"text": "function", "is_correct": False},
                    {"text": "func", "is_correct": False},
                    {"text": "def", "is_correct": True},
                    {"text": "define", "is_correct": False},
                ]
            },
            {
                "question_text": "return kalit so'zi nimaga xizmat qiladi?",
                "explanation": "return — funksiyadan qiymat qaytaradi. return dan keyin funksiya bajarilishini to'xtatadi.",
                "choices": [
                    {"text": "Funksiyani e'lon qiladi", "is_correct": False},
                    {"text": "Funksiyani chaqiradi", "is_correct": False},
                    {"text": "Funksiyadan qiymat qaytaradi va funksiyani to'xtatadi", "is_correct": True},
                    {"text": "Faqat funksiyani to'xtatadi", "is_correct": False},
                ]
            },
            {
                "question_text": "Quyidagi funksiya qanday natija chiqaradi?\n\ndef ko_pay(x, y):\n    return x * y\n\nprint(ko_pay(3, 4))",
                "explanation": "3 * 4 = 12, funksiya 12 ni qaytaradi va print chiqaradi.",
                "choices": [
                    {"text": "7", "is_correct": False},
                    {"text": "34", "is_correct": False},
                    {"text": "12", "is_correct": True},
                    {"text": "Xato", "is_correct": False},
                ]
            },
            {
                "question_text": "Default parametr nima?",
                "explanation": "Default parametr — funksiya chaqirilganda qiymat berilmasa ishlatiluvchi oldindan belgilangan qiymat.",
                "choices": [
                    {"text": "Har doim majburiy beriladigan parametr", "is_correct": False},
                    {"text": "Funksiya chaqirilganda qiymat berilmasa ishlatiluvchi standart qiymat", "is_correct": True},
                    {"text": "Faqat bitta bo'lishi mumkin bo'lgan parametr", "is_correct": False},
                    {"text": "Funksiyaning qaytarish qiymati", "is_correct": False},
                ]
            },
            {
                "question_text": "Lambda funksiya nima?",
                "explanation": "Lambda — bitta ifodadan iborat anonim (nomsiz) funksiya. lambda x: x*2 kabi yoziladi.",
                "choices": [
                    {"text": "Ko'p qatorli murakkab funksiya", "is_correct": False},
                    {"text": "Bitta ifodadan iborat anonim funksiya", "is_correct": True},
                    {"text": "Faqat rekursiv funksiya", "is_correct": False},
                    {"text": "Modul ichidagi funksiya", "is_correct": False},
                ]
            },
            {
                "question_text": "Quyidagi kod qanday natija beradi?\n\ndef salom(ism='Do'st'):\n    return f'Salom, {ism}!'\n\nprint(salom())",
                "explanation": "Funksiya ism parametrisiz chaqirilgan, shuning uchun default qiymat 'Do'st' ishlatiladi.",
                "choices": [
                    {"text": "Salom, !", "is_correct": False},
                    {"text": "Salom, Do'st!", "is_correct": True},
                    {"text": "Xato (parametr berilmagan)", "is_correct": False},
                    {"text": "None", "is_correct": False},
                ]
            },
        ]
    },

    # ── Dars 6: Ro'yxatlar (List) ──────────────────────────────
    "6. Ma'lumotlar tuzilmalari: ro'yxatlar (list)": {
        "quiz_title": "Ro'yxatlar (List) — nazariy test",
        "questions": [
            {
                "question_text": "Python da ro'yxat (list) qanday e'lon qilinadi?",
                "explanation": "Ro'yxat kvadrat qavslar [] ichida vergul bilan ajratilgan elementlar orqali e'lon qilinadi.",
                "choices": [
                    {"text": "ro'yxat = (1, 2, 3)", "is_correct": False},
                    {"text": "ro'yxat = [1, 2, 3]", "is_correct": True},
                    {"text": "ro'yxat = {1, 2, 3}", "is_correct": False},
                    {"text": "ro'yxat = <1, 2, 3>", "is_correct": False},
                ]
            },
            {
                "question_text": "ro'yxat = [10, 20, 30, 40]. ro'yxat[2] qanday qiymat beradi?",
                "explanation": "Python da indeks 0 dan boshlanadi. indeks 2 — 3-element, ya'ni 30.",
                "choices": [
                    {"text": "20", "is_correct": False},
                    {"text": "30", "is_correct": True},
                    {"text": "40", "is_correct": False},
                    {"text": "Xato", "is_correct": False},
                ]
            },
            {
                "question_text": "Ro'yxatga yangi element qo'shish uchun qaysi metod ishlatiladi?",
                "explanation": "append() metodi ro'yxat oxiriga yangi element qo'shadi.",
                "choices": [
                    {"text": "add()", "is_correct": False},
                    {"text": "insert()", "is_correct": False},
                    {"text": "append()", "is_correct": True},
                    {"text": "push()", "is_correct": False},
                ]
            },
            {
                "question_text": "len([1, 2, 3, 4, 5]) qanday natija qaytaradi?",
                "explanation": "len() funksiyasi ro'yxatdagi elementlar sonini qaytaradi. Bu ro'yxatda 5 element bor.",
                "choices": [
                    {"text": "4", "is_correct": False},
                    {"text": "5", "is_correct": True},
                    {"text": "6", "is_correct": False},
                    {"text": "Xato", "is_correct": False},
                ]
            },
            {
                "question_text": "ro'yxat = [3, 1, 4, 1, 5]. ro'yxat[-1] nima qaytaradi?",
                "explanation": "Manfiy indeks oxirdan hisoblaydi. -1 oxirgi element, ya'ni 5.",
                "choices": [
                    {"text": "3", "is_correct": False},
                    {"text": "1", "is_correct": False},
                    {"text": "5", "is_correct": True},
                    {"text": "Xato (manfiy indeks ishlamaydi)", "is_correct": False},
                ]
            },
            {
                "question_text": "ro'yxat = [1, 2, 3]. ro'yxat.remove(2) dan so'ng ro'yxat qanday ko'rinadi?",
                "explanation": "remove() metodi ro'yxatdan birinchi uchraydigan berilgan qiymatni o'chiradi.",
                "choices": [
                    {"text": "[1, 2]", "is_correct": False},
                    {"text": "[1, 3]", "is_correct": True},
                    {"text": "[2, 3]", "is_correct": False},
                    {"text": "[1, 2, 3]", "is_correct": False},
                ]
            },
        ]
    },

    # ── Dars 7: Lug'atlar (Dictionary) ─────────────────────────
    "7. Lug'atlar (dictionary) bilan ishlash": {
        "quiz_title": "Lug'atlar (Dictionary) — nazariy test",
        "questions": [
            {
                "question_text": "Python da lug'at (dictionary) qanday e'lon qilinadi?",
                "explanation": "Lug'at jingalak qavslar {} ichida kalit:qiymat juftliklari bilan e'lon qilinadi.",
                "choices": [
                    {"text": "d = [kalit, qiymat]", "is_correct": False},
                    {"text": "d = (kalit: qiymat)", "is_correct": False},
                    {"text": "d = {'kalit': 'qiymat'}", "is_correct": True},
                    {"text": "d = <kalit: qiymat>", "is_correct": False},
                ]
            },
            {
                "question_text": "d = {'ism': 'Ali', 'yosh': 20}. d['ism'] qanday natija beradi?",
                "explanation": "Lug'atdan kalit orqali qiymat olinadi. 'ism' kaliti 'Ali' qiymatini qaytaradi.",
                "choices": [
                    {"text": "20", "is_correct": False},
                    {"text": "'Ali'", "is_correct": True},
                    {"text": "{'ism': 'Ali'}", "is_correct": False},
                    {"text": "Xato", "is_correct": False},
                ]
            },
            {
                "question_text": "Lug'atdagi barcha kalitlarni olish uchun qaysi metod ishlatiladi?",
                "explanation": "keys() metodi lug'atdagi barcha kalitlarni qaytaradi.",
                "choices": [
                    {"text": "d.values()", "is_correct": False},
                    {"text": "d.items()", "is_correct": False},
                    {"text": "d.keys()", "is_correct": True},
                    {"text": "d.all()", "is_correct": False},
                ]
            },
            {
                "question_text": "Lug'atga yangi juftlik qo'shish uchun nima qilish kerak?",
                "explanation": "d['yangi_kalit'] = 'yangi_qiymat' ko'rinishida yangi juftlik qo'shiladi.",
                "choices": [
                    {"text": "d.add('yangi_kalit', 'yangi_qiymat')", "is_correct": False},
                    {"text": "d['yangi_kalit'] = 'yangi_qiymat'", "is_correct": True},
                    {"text": "d.append({'yangi_kalit': 'yangi_qiymat'})", "is_correct": False},
                    {"text": "d.insert('yangi_kalit', 'yangi_qiymat')", "is_correct": False},
                ]
            },
            {
                "question_text": "d = {'a': 1, 'b': 2}. 'c' in d ifodasi qanday natija beradi?",
                "explanation": "in operatori lug'atda kalit borligini tekshiradi. 'c' kaliti yo'q, shuning uchun False.",
                "choices": [
                    {"text": "True", "is_correct": False},
                    {"text": "False", "is_correct": True},
                    {"text": "None", "is_correct": False},
                    {"text": "Xato", "is_correct": False},
                ]
            },
            {
                "question_text": "d.get('mavjudemas', 'standart') — agar kalit topilmasa nima qaytaradi?",
                "explanation": "get() metodi kalit topilmasa ikkinchi argument sifatida berilgan standart qiymatni qaytaradi.",
                "choices": [
                    {"text": "None", "is_correct": False},
                    {"text": "Xato (KeyError)", "is_correct": False},
                    {"text": "'standart'", "is_correct": True},
                    {"text": "False", "is_correct": False},
                ]
            },
        ]
    },

    # ── Dars 8: OOP ─────────────────────────────────────────────
    "8. Python da OOP ga kirish": {
        "quiz_title": "Ob'yektga Yo'naltirilgan Dasturlash (OOP) — nazariy test",
        "questions": [
            {
                "question_text": "Python da klass (class) qanday e'lon qilinadi?",
                "explanation": "class kalit so'zi bilan klass e'lon qilinadi va odatda PascalCase qoidasida nomlanadi.",
                "choices": [
                    {"text": "Class Mashina: (katta harf bilan kalit so'z)", "is_correct": False},
                    {"text": "class Mashina:", "is_correct": True},
                    {"text": "new class Mashina()", "is_correct": False},
                    {"text": "define class Mashina", "is_correct": False},
                ]
            },
            {
                "question_text": "__init__ metodi nima uchun ishlatiladi?",
                "explanation": "__init__ — konstruktor metodi bo'lib, ob'yekt yaratilganda avtomatik chaqiriladi va xossalarni boshlang'ich qiymat bilan to'ldiradi.",
                "choices": [
                    {"text": "Ob'yektni o'chirish uchun", "is_correct": False},
                    {"text": "Ob'yekt yaratilganda avtomatik chaqiriladigan konstruktor", "is_correct": True},
                    {"text": "Faqat xossalarni ko'rsatish uchun", "is_correct": False},
                    {"text": "Metodlarni import qilish uchun", "is_correct": False},
                ]
            },
            {
                "question_text": "self parametri nima?",
                "explanation": "self — joriy ob'yektning o'ziga havola. Metodlar orqali ob'yektning xossalariga self.nom ko'rinishida murojaat qilinadi.",
                "choices": [
                    {"text": "Klassning nomi", "is_correct": False},
                    {"text": "Joriy ob'yektga havola", "is_correct": True},
                    {"text": "Majburiy qiymat berilishi kerak bo'lgan parametr", "is_correct": False},
                    {"text": "Maxsus kalit so'z faqat __init__ uchun", "is_correct": False},
                ]
            },
            {
                "question_text": "Meros olish (inheritance) qanday yoziladi?",
                "explanation": "class Bola(Ota): ko'rinishida meros olinadi — qavslar ichida ota klass nomi yoziladi.",
                "choices": [
                    {"text": "class Bola extends Ota:", "is_correct": False},
                    {"text": "class Bola inherits Ota:", "is_correct": False},
                    {"text": "class Bola(Ota):", "is_correct": True},
                    {"text": "class Bola: extends(Ota)", "is_correct": False},
                ]
            },
            {
                "question_text": "Encapsulation (inkapsulyatsiya) nimani anglatadi?",
                "explanation": "Inkapsulyatsiya — ma'lumotlarni va metodlarni bitta ob'yekt ichiga yashirish va tashqi kirishni cheklash.",
                "choices": [
                    {"text": "Bir klassdan boshqa klass yaratish", "is_correct": False},
                    {"text": "Metodlarni qayta ishlash", "is_correct": False},
                    {"text": "Ma'lumotlar va metodlarni birlashtirish va ichki ma'lumotni yashirish", "is_correct": True},
                    {"text": "Kodni ko'p marta ishlatish", "is_correct": False},
                ]
            },
            {
                "question_text": "Quyidagi kod qanday natija beradi?\n\nclass It:\n    def __init__(self, ism):\n        self.ism = ism\n    def hurish(self):\n        return f'{self.ism} vov-vov!'\n\nit = It('Bars')\nprint(it.hurish())",
                "explanation": "It klassi 'Bars' ismi bilan yaratilgan, hurish() metodi 'Bars vov-vov!' qaytaradi.",
                "choices": [
                    {"text": "vov-vov!", "is_correct": False},
                    {"text": "Bars vov-vov!", "is_correct": True},
                    {"text": "It('Bars')", "is_correct": False},
                    {"text": "Xato", "is_correct": False},
                ]
            },
        ]
    },

    # ── Dars 9: Modullar va paketlar ───────────────────────────
    "9. Modullar va paketlar": {
        "quiz_title": "Modullar va paketlar — nazariy test",
        "questions": [
            {
                "question_text": "Python da modul import qilish uchun qaysi kalit so'z ishlatiladi?",
                "explanation": "import kalit so'zi Python modullarini dasturga ulash uchun ishlatiladi.",
                "choices": [
                    {"text": "include", "is_correct": False},
                    {"text": "require", "is_correct": False},
                    {"text": "import", "is_correct": True},
                    {"text": "use", "is_correct": False},
                ]
            },
            {
                "question_text": "Moduldan faqat bitta funksiyani import qilish uchun qanday yoziladi?",
                "explanation": "from modul import funksiya — faqat kerakli funksiya import qilinadi.",
                "choices": [
                    {"text": "import funksiya from modul", "is_correct": False},
                    {"text": "from modul import funksiya", "is_correct": True},
                    {"text": "modul.import(funksiya)", "is_correct": False},
                    {"text": "import modul.funksiya", "is_correct": False},
                ]
            },
            {
                "question_text": "import math dan so'ng ildiz hisoblash uchun qaysi buyruq ishlatiladi?",
                "explanation": "math.sqrt() funksiyasi sonning kvadrat ildizini hisoblaydi.",
                "choices": [
                    {"text": "math.root(9)", "is_correct": False},
                    {"text": "sqrt(9)", "is_correct": False},
                    {"text": "math.sqrt(9)", "is_correct": True},
                    {"text": "math.square(9)", "is_correct": False},
                ]
            },
            {
                "question_text": "import random; random.randint(1, 10) nima qaytaradi?",
                "explanation": "randint(a, b) — a va b (ikkalasi ham kiritilgan) orasidagi tasodifiy butun son qaytaradi.",
                "choices": [
                    {"text": "1 dan 9 oralig'idagi son (10 kiritilmaydi)", "is_correct": False},
                    {"text": "1 dan 10 oralig'idagi tasodifiy butun son (10 ham kiritiladi)", "is_correct": True},
                    {"text": "Har doim 5 ni qaytaradi", "is_correct": False},
                    {"text": "Haqiqiy son (float) qaytaradi", "is_correct": False},
                ]
            },
            {
                "question_text": "Python da o'z modulingizni yaratish uchun nima qilish kerak?",
                "explanation": ".py kengaytmali fayl yaratib, unga funksiya va klasslar yozsangiz — bu Python moduli bo'ladi.",
                "choices": [
                    {"text": "Maxsus kutubxona o'rnatish kerak", "is_correct": False},
                    {"text": ".py kengaytmali fayl yaratib, ichiga kod yozish kifoya", "is_correct": True},
                    {"text": "Faqat standart kutubxonalar ishlatilishi mumkin", "is_correct": False},
                    {"text": "__module__ = True yozish kerak", "is_correct": False},
                ]
            },
            {
                "question_text": "import datetime; datetime.datetime.now() nima qaytaradi?",
                "explanation": "datetime.now() hozirgi sana va vaqtni (yil, oy, kun, soat, minut, sekund) qaytaradi.",
                "choices": [
                    {"text": "Faqat bugungi sanani", "is_correct": False},
                    {"text": "Faqat joriy vaqtni", "is_correct": False},
                    {"text": "Joriy sana va vaqtni birga", "is_correct": True},
                    {"text": "Xato (parametr kerak)", "is_correct": False},
                ]
            },
        ]
    },

    # ── Dars 10: Xatolarni qayta ishlash ───────────────────────
    "10. Xatolarni qayta ishlash (try-except)": {
        "quiz_title": "Xatolarni qayta ishlash — nazariy test",
        "questions": [
            {
                "question_text": "Python da xatolarni ushlab olish uchun qaysi konstruktsiya ishlatiladi?",
                "explanation": "try-except bloki xatolarni ushlab olish va qayta ishlash uchun ishlatiladi.",
                "choices": [
                    {"text": "try { } catch { }", "is_correct": False},
                    {"text": "try: ... except:", "is_correct": True},
                    {"text": "catch: ... handle:", "is_correct": False},
                    {"text": "error: ... fix:", "is_correct": False},
                ]
            },
            {
                "question_text": "ZeroDivisionError qachon yuz beradi?",
                "explanation": "Sonni 0 ga bo'lmoqchi bo'lganda ZeroDivisionError xatosi yuzaga keladi.",
                "choices": [
                    {"text": "O'zgaruvchi topilmaganda", "is_correct": False},
                    {"text": "Sonni 0 ga bo'lganda", "is_correct": True},
                    {"text": "Fayl topilmaganda", "is_correct": False},
                    {"text": "Noto'g'ri xotira manzilida", "is_correct": False},
                ]
            },
            {
                "question_text": "finally bloki qachon bajariladi?",
                "explanation": "finally bloki xato bo'lsa ham, bo'lmasa ham — har doim bajariladi. Tozalash operatsiyalari uchun ishlatiladi.",
                "choices": [
                    {"text": "Faqat xato bo'lganda", "is_correct": False},
                    {"text": "Faqat xato bo'lmaganda", "is_correct": False},
                    {"text": "Har doim — xato bo'lsa ham bo'lmasa ham", "is_correct": True},
                    {"text": "Hech qachon bajarilmaydi", "is_correct": False},
                ]
            },
            {
                "question_text": "raise kalit so'zi nima uchun ishlatiladi?",
                "explanation": "raise — dasturchi tomonidan qo'lda xato chaqirish uchun ishlatiladi.",
                "choices": [
                    {"text": "Xatoni ushlab olish uchun", "is_correct": False},
                    {"text": "Xatoni o'chirish uchun", "is_correct": False},
                    {"text": "Qo'lda (manually) xato chaqirish uchun", "is_correct": True},
                    {"text": "Dasturni to'xtatish uchun", "is_correct": False},
                ]
            },
            {
                "question_text": "Quyidagi kod qanday natija beradi?\n\ntry:\n    x = 10 / 0\nexcept ZeroDivisionError:\n    print('Xato!')\nfinally:\n    print('Tamom')",
                "explanation": "10/0 ZeroDivisionError beradi, except bloki 'Xato!' chiqaradi, finally har doim 'Tamom' chiqaradi.",
                "choices": [
                    {"text": "Faqat 'Xato!'", "is_correct": False},
                    {"text": "Faqat 'Tamom'", "is_correct": False},
                    {"text": "'Xato!' keyin 'Tamom'", "is_correct": True},
                    {"text": "Dastur to'xtaydi xatoliksiz", "is_correct": False},
                ]
            },
            {
                "question_text": "TypeError qachon yuzaga keladi?",
                "explanation": "TypeError noto'g'ri turda operatsiya bajarilganda yuzaga keladi, masalan '5' + 3 (matn + son).",
                "choices": [
                    {"text": "O'zgaruvchi topilmaganda", "is_correct": False},
                    {"text": "Noto'g'ri turda operatsiya bajarilganda (masalan, matn + son)", "is_correct": True},
                    {"text": "0 ga bo'linganda", "is_correct": False},
                    {"text": "Cheksiz rekursiyada", "is_correct": False},
                ]
            },
        ]
    },

}


class Command(BaseCommand):
    help = "Har bir dars uchun kamida 5 ta nazariy test savoli qo'shadi"

    def add_arguments(self, parser):
        parser.add_argument(
            '--lesson-id', dest='lesson_id', type=int, default=None,
            help="Faqat bitta darsga qo'shish (ID bo'yicha)"
        )
        parser.add_argument(
            '--force', action='store_true',
            help="Mavjud quizlarni o'chirib qayta yozadi"
        )

    def handle(self, *args, **options):
        lesson_id = options['lesson_id']
        force     = options['force']

        if lesson_id:
            lessons = Lesson.objects.filter(id=lesson_id)
        else:
            lessons = Lesson.objects.all().order_by('order')

        if not lessons.exists():
            self.stdout.write(self.style.ERROR("Hech qanday dars topilmadi."))
            return

        total_added = 0
        total_skipped = 0

        for lesson in lessons:
            # Dars nomi bo'yicha ma'lumot qidirish
            quiz_data = None
            for key, data in QUIZZES_DATA.items():
                if key in lesson.title:
                    quiz_data = data
                    break

            if not quiz_data:
                self.stdout.write(
                    self.style.WARNING(f"  [!] [{lesson.id}] '{lesson.title}' uchun savollar topilmadi - o'tkazib yuborildi.")
                )
                total_skipped += 1
                continue

            # Agar force bo'lsa va quiz mavjud bo'lsa — uni o'chirib qayta yozamiz
            existing = lesson.quizzes.filter(title=quiz_data['quiz_title'])
            if existing.exists():
                if force:
                    existing.delete()
                    self.stdout.write(f"  [DEL]  Mavjud quiz o'chirildi: '{quiz_data['quiz_title']}'")
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"  [SKIP]  [{lesson.id}] '{lesson.title}' - quiz mavjud, o'tkazildi (--force yozing qayta yozish uchun)"
                        )
                    )
                    total_skipped += 1
                    continue

            # Quiz yaratish
            next_order = lesson.quizzes.count() + 1
            quiz = Quiz.objects.create(
                lesson=lesson,
                title=quiz_data['quiz_title'],
                order=next_order,
            )

            for i, q in enumerate(quiz_data['questions'], 1):
                question = QuizQuestion.objects.create(
                    quiz=quiz,
                    question_text=q['question_text'],
                    question_type='multiple_choice',
                    explanation=q['explanation'],
                    order=i,
                )
                for c in q['choices']:
                    QuizChoice.objects.create(
                        question=question,
                        choice_text=c['text'],
                        is_correct=c['is_correct'],
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f"  [OK] [{lesson.id}] {lesson.title} - {len(quiz_data['questions'])} ta savol qo'shildi"
                )
            )
            total_added += 1

        self.stdout.write("\n" + "-" * 60)
        self.stdout.write(self.style.SUCCESS(f"Jami: {total_added} ta darsga quiz qo'shildi"))
        if total_skipped:
            self.stdout.write(self.style.WARNING(f"[SKIP] {total_skipped} ta dars o'tkazildi"))
        self.stdout.write("-" * 60)
