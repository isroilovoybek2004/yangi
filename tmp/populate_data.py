import os
import sys
import django

# Project root-ni PYTHONPATH-ga qo'shish
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Django muhitini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from courses.models import Course
from lessons.models import Lesson, Task

User = get_user_model()

def populate():
    print("Eski bazani tozalash...")
    Course.objects.all().delete()
    print("Boshqaruv rollarini yaratish...")
    admin_user, created = User.objects.get_or_create(username='admin')
    if created:
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print(f"Yangi Admin yaratildi: {admin_user.username}")

    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from progress.models import Progress, Submission
    
    teacher_group, created = Group.objects.get_or_create(name='Ustozlar')
    if created:
        for model in [Course, Lesson, Task, Quiz, QuizQuestion, QuizChoice]:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct)
            for perm in perms:
                teacher_group.permissions.add(perm)
        
        # O'quvchilar progressini ko'rish (faqat ko'rish)
        for model in [Progress, Submission, User]:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(content_type=ct, codename__startswith='view_')
            for perm in perms:
                teacher_group.permissions.add(perm)

    instructor, created = User.objects.get_or_create(username='testuser')
    if created:
        instructor.set_password('password123')
        instructor.is_staff = True
        instructor.is_superuser = False
        instructor.save()
        instructor.groups.add(teacher_group)
        print(f"Yangi o'qituvchi yaratildi: {instructor.username}")

    course = Course.objects.create(
        title="Python dasturlash asoslari (to'liq kurs)",
        instructor=instructor,
        description="Python dasturlash tilini noldan mukammal o'rganish uchun mo'ljallangan interaktiv va to'liq qo'llanma."
    )
    print(f"Kurs yaratildi: {course.title}")

    lessons_data = [
        {
            "title": "1. Kirish va Python haqida tushuncha",
            "content": """
            <h2>Python nimaga kerak?</h2>
            
            <div class="video-wrapper">
                <iframe src="https://www.youtube.com/embed/Z1Yd7upQsXY?si=tM3Hk6O1eT4Z-t2v" title="Python tili imkoniyatlari" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
            </div>

            <p><strong>Python</strong> — dunyodagi eng mashhur, o'rganish uchun sodda va shu bilan birga juda qudratli dasturlash tillaridan biri hisoblanadi. Uning sintaksisi (yozilish qoidalari) inson tiliga juda yaqin bo'lib, o'qish va tushunishni osonlashtiradi.</p>
            
            <h3>Python qayerlarda ishlatiladi?</h3>
            
            <!-- Safe CSS Animation Replacement -->
            <div class="typing-demo">Hacking with Python...</div>

            <ul>
                <li><strong>Veb-dasturlash:</strong> backend qismida (Django, Flask kabi freymvorklar orqali).</li>
                <li><strong>Sun'iy intelekt va Data Science:</strong> ma'lumotlarni tahlil qilish va AI yaratishda.</li>
                <li><strong>Avtomatlashtirish:</strong> kundalik zerikarli ishlarni kompyuterga topshirish.</li>
            </ul>
            
            <h3>Birinchi dasturingiz: 'Salom, dunyo!'</h3>
            <p>Dasturlash olamida o'rganishni har doim ekranga salomlashish so'zini chiqarish bilan boshlash o'ziga xos an'anaga aylangan. Pythonda ma'lumotni ekranga chiqarish uchun <code class="animate-pulse">print()</code> (chop etish) funksiyasi ishlatiladi.</p>
            
            <pre><code>print("Salom, Dunyo!")</code></pre>
            
            <p><strong>E'tibor bering:</strong> Matnlar har doim qo'shtirnoq <code>" "</code> yoki bittalik tirnoq <code>' '</code> ichida yozilishi shart.</p>
            """,
            "tasks": [
                {
                    "title": "Birinchi qadam",
                    "question": "Ekranga 'Salom dunyo' yozuvini chiqaruvchi dastur tuzing.",
                    "expected_output": "Salom dunyo",
                    "ai_hints": "print('Matnbu') funksiyasidan foydalaning, matn qo'shtirnoq ichida bo'lsin."
                },
                {
                    "title": "O'zingizni tanishtiring",
                    "question": "Ekranga 'Men Python o'rganyapman!' yozuvini chiqaring.",
                    "expected_output": "Men Python o'rganyapman!",
                    "ai_hints": "Avvalgidek print() funksiyasidan foydalanib o'zgartirilgan matnni yozing."
                },
                {
                    "title": "Matematik amal",
                    "question": "Pythonda matn emas, balki sonlarni ham chiqarish mumkin. Ekranga 2026 sonini chiqaring.",
                    "expected_output": "2026",
                    "ai_hints": "Sonlarni qo'shtirnoqsiz to'g'ridan-to'g'ri yozish mumkin: print(raqam)"
                }
            ]
        },
        {
            "title": "2. O'zgaruvchilar va Ma'lumot Turlari",
            "content": """
            <h2>O'zgaruvchilar (Variables)</h2>
            <p>O'zgaruvchi — bu kompyuter xotirasidagi ma'lumotni saqlab turuvchi quti (konteyner). Kodda har doim uzundan-uzoq sonlarni yoki matnlarni yozish noqulay, shuning uchun biz ularga nom beramiz.</p>
            
            <!-- Safe CSS Animation Replacement -->
            <div class="box-demo">
                <div class="box-value">42</div>
            </div>

            <pre><code>ism = "Ali"
yosh = 20
print(ism)
print(yosh)</code></pre>

            <h3>Ma'lumot turlari (Data Types)</h3>
            <div class="video-wrapper">
                <iframe src="https://www.youtube.com/embed/khKv-8q7YmY" title="Python ma'lumot turlari" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
            </div>

            <p>Pythonda asosan quyidagi ma'lumot turlari ko'p ishlatiladi:</p>
            <ul>
                <li><code>int</code> (Integer) - Butun sonlar: 5, -10, 1000</li>
                <li><code>float</code> (Float) - O'nlik (haqiqiy) sonlar: 3.14, -2.5</li>
                <li><code>str</code> (String) - Matnlar: "Salom", 'Python'</li>
                <li><code>bool</code> (Boolean) - Mantiqiy qiymatlar: True (Rost), False (Yolg'on)</li>
            </ul>
            
            <p>Pythonda <strong>Typecasting</strong> (ma'lumot turini o'zgartirish) mumkin. Masalan, matn ko'rinishidagi sonni haqiqiy songa o'tkazish: <code>int("10")</code> qilsak bu matnni 10 raqamiga aylantirib beradi.</p>
            """,
            "tasks": [
                {
                    "title": "O'zgaruvchi yaratish",
                    "question": "a = 5 va b = 10 ekanligini e'lon qiling, so'ngra ularning yig'indisini ekranga chiqaring.",
                    "expected_output": "15",
                    "ai_hints": "a va b uchun qiymatlar bering. Keyin print(a + b) kabi hisoblang."
                },
                {
                    "title": "Matnlarni qo'shish (konkatenatsiya)",
                    "question": "ism = 'Ali' va familiya = 'Valiyev' o'zgaruvchilarini s=ism+' '+familiya qilib qo'shing. Natijaviy o'zgaruvchini chop eting (Ali Valiyev).",
                    "expected_output": "Ali Valiyev",
                    "ai_hints": "Matnlarni qo'shish uchun '+' belgisidan foydalanamiz, o'rtada bo'sh joy qo'shish esdan chiqmasin."
                },
                {
                    "title": "Turini almashtirish",
                    "question": "x = '100' (bu hozir matn). Uni 'int()' orqali butun songa aylantiring va unga 50 ni qo'shib ekranga chiqaring natija tasviri sifatida.",
                    "expected_output": "150",
                    "ai_hints": "yangi_x = int(x) qiling va keyin unga 50 qo'shib chop eting."
                }
            ]
        },
        {
            "title": "3. Shartli Operatorlar (if, elif, else)",
            "content": """
            <h2>Qaror qabul qilish (Conditions)</h2>
            <p>Dasturlar har doim ham bitta tekislikda ishlamaydi. Ko'pincha qandaydir shartlarga tekshirish talab etiladi. Buning uchun Pythonda <code>if</code> (agar), <code>elif</code> (yoki agar), va <code>else</code> (aks holda) so'zlaridan foydalaniladi.</p>
            
            <!-- Safe CSS Box logic representation -->
            <pre style="text-align:center; padding: 20px; font-weight:bold; border: 2px solid var(--accent); background: rgba(59, 130, 246, 0.1); border-radius: 8px;">
Agar (Yomir yog'sa):
  Zontikni oling! ☔
Aks holda:
  Bosh kiyim kiying! 🧢
            </pre>

            <h3>Tuzilishi:</h3>
            <pre><code>parol = "maxfiy"
if parol == "maxfiy":
    print("Xush kelibsiz!")
else:
    print("Parol nato'g'ri.")</code></pre>
            
            <div class="video-wrapper">
                <iframe src="https://www.youtube.com/embed/AWek4Yv0Krs" title="Python if else operatorlari" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
            </div>

            <p><strong>E'tibor bering:</strong> <code>if</code> yozilgan qator yakunlanishida <code>:</code> (ikki nuqta) qo'yiladi va keyingi qator albatta bitta chekinga ega bo'lishi (Indentation - 4ta bo'sh joy) kerak. Python kodning bir-biriga qaramligini aynan shu joy tashlashlaridan bilib oladi.</p>
            
            <h3>Mantiqiy operatorlar:</h3>
            <p>Siz bir nechta shartni biriktirish uchun <code>and</code> (va), <code>or</code> (yoki), <code>not</code> (inkor) so'zlaridan foydalanishingiz mumkin. Yana taqqoslash uchu <code>&gt;</code>, <code>&lt;</code>, <code>&gt;=</code>, <code>&lt;=</code>, <code>==</code> (teng), <code>!=</code> (teng emas) lar mavjud.</p>
            """,
            "tasks": [
                {
                    "title": "Shartga tekshirish",
                    "question": "x = 7. Agar x 0 dan katta bo'lsa ekranga 'Musbat' deb chiqaring.",
                    "expected_output": "Musbat",
                    "ai_hints": "if x > 0: deb yozing, va keyingi qatorda biroz bo'sh joy tashlab print yozing."
                },
                {
                    "title": "Else dan foydalanish",
                    "question": "y = -5. Agar y 0 dan katta yoki teng bo'lsa 'Musbat', aks holda (else) 'Manfiy' deb chiqaring.",
                    "expected_output": "Manfiy",
                    "ai_hints": "if y >= 0: ... else: ... ko'rinishida yozing."
                },
                {
                    "title": "Juft yoki toq",
                    "question": "son = 10. Agar son 2 ga qoldiqsiz bo'linsa (son % 2 == 0) 'Juft', aks holda 'Toq' yozuvini chiqaring.",
                    "expected_output": "Juft",
                    "ai_hints": "Bo'linmaning qoldig'ini topish uchun '%' operatoridan foydalaniladi. Agar son % 2 == 0 bo'lsa demak u juft."
                }
            ]
        },
        {
            "title": "4. Sikllar (for va while)",
            "content": """
            <h2>Takrorlanuvchi jarayonlar (Loops)</h2>
            <p>Aytaylik, biror amalni 100 marta bajarishingiz kerak. 100 qator kod yozish o'rniga biz tsikllardan (loop) foydalanamiz. Pythonda ikkita asosiy tsikl mavjud: <strong>for</strong> va <strong>while</strong>.</p>
            
            <!-- Safe CSS Loop Animation Replacement -->
            <div class="loop-demo">
                <div class="loop-item">1</div>
                <div class="loop-item">2</div>
                <div class="loop-item">3</div>
                <div class="loop-item">4</div>
            </div>

            <h3>For tsikli</h3>
            <p><code>for</code> odatda qandaydir xudud yoki to'plam bo'ylab aylanib chiqish uchun ishlatiladi. Eng ko'p <code>range()</code> (oraliq) funksiyasi bilan birga uchraydi.</p>
            <pre><code>for i in range(1, 4):
    print(i) # 1, 2, 3 chiqadi</code></pre>
    
            <div class="video-wrapper">
                <iframe src="https://www.youtube.com/embed/6iF8Xb7Z3wQ" title="Python For Loop" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
            </div>

            <h3>While tsikli</h3>
            <p><code>while</code> (toki... gacha) esa berilgan shart to'g'ri (True) bo'lib turguniga qadar ishlashda davom etaveradi.</p>
            <pre><code>k = 1
while k &lt;= 3:
    print(k)
    k += 1 # k ni 1 taga oshiramiz</code></pre>
            
            <p>Dastur qotib qolmasligi uchun (Infinity Loop), <code>while</code> tsikli ishlashini to'xtatadigan holatga hamisha e'tibor qaratish kerak.</p>
            """,
            "tasks": [
                {
                    "title": "Har bir qatorda raqam chiqarish",
                    "question": "for sikli va range() dan foydalanib 1 dan 5 gacha bo'lgan sonlarni har birini alohida qatorda ekranga chiqaring.",
                    "expected_output": "1\n2\n3\n4\n5",
                    "ai_hints": "range(1, 6) ni bersangiz 1,2,3,4,5 sonlarini ishlab chiqaradi."
                },
                {
                    "title": "Faqat juft sonlarni chiqarish",
                    "question": "for siklidan foydalanib 2 dan 10 gacha (10 ni o'zi ham kiradi) bo'lgan barcha juft sonlarni alohida qatorda chiqaring.",
                    "expected_output": "2\n4\n6\n8\n10",
                    "ai_hints": "range(2, 11, 2) ni ishlating. Uchinchi parametr qadam (qanchaga oshish) vazifasini bajaradi."
                },
                {
                    "title": "While dan foydalanish",
                    "question": "k = 3. while siklidan foydalanib k > 0 gacha k ni ekranga chiqaring. Har takrorlanishda k ni 1 taga kamaytirib boring (k -= 1).",
                    "expected_output": "3\n2\n1",
                    "ai_hints": "while k > 0: deb boshlang, va har safar k ni qiymatini o'zgartirishni unutmang."
                }
            ]
        },
        {
            "title": "5. Funksiyalar bilan ishlash",
            "content": """
            <h2>Funksiyalar (Functions)</h2>
            <p>Qayta-qayta ishlatiladigan kod bloklarini bitta qolipga solish — funksiya deb ataladi. U dasturni ixcham va o'qish uchun qulay qilib beradi. Pythonda funksiyalar <code>def</code> kalit so'zi vositasida e'lon qilinadi.</p>
            
            <!-- Function visualization -->
            <pre style="text-align:center; padding: 20px; font-weight:bold; border: 2px dashed var(--primary); background: rgba(59, 130, 246, 0.05); border-radius: 8px;">
Input (x) ➔ [ F(x) Hisoblash ] ➔ Output (Natija)
            </pre>

            <h3>Tuzilishi:</h3>
            <pre><code>def salom_ber(ism):
    print("Salom, " + ism)
    
# Funksiyani chaqirish (ishga tushirish)
salom_ber("Ali")
salom_ber("Vali")</code></pre>

            <div class="video-wrapper">
                <iframe src="https://www.youtube.com/embed/9Os0o3wzS_I" title="Python def Functions" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
            </div>

            <p>Funksiyalar parametr qabul qilishi (ism) va qandaydir hisob-kitob qilib, <code>return</code> orqali asosiy dasturga javob qaytarishi ham mumkin.</p>
            <pre><code>def qosh(a, b):
    javob = a + b
    return javob

print(qosh(10, 5)) # 15 chiqadi</code></pre>
            """,
            "tasks": [
                {
                    "title": "Kvadratga oshirish funksiyasi",
                    "question": "kvadrat(n) funksiyasini e'lon qiling, u olingan sonning(n) kvadratini 'return' orqali qaytarsin. Eng oxirida kvadrat(4) ni print yordamida chop eting.",
                    "expected_output": "16",
                    "ai_hints": "def kvadrat(n): return n * n shaklida funksiya yozib so'ng uni ishlating."
                },
                {
                    "title": "Eng kattasini topish",
                    "question": "eng_katta(a, b) nomli funksiya yozing, agar a katta bo'lsa a ni, aks holda b ni return qilsin. eng_katta(10, 20) ni print qiling.",
                    "expected_output": "20",
                    "ai_hints": "Funksiya ichida if a > b: return a ... else ... return b ko'rinishida qo'llash mumkin."
                },
                {
                    "title": "Salomlashish",
                    "question": "salom_ber(ism) deb e'lon qilinsin, u \"Assalomu alaykum, X\" matnini return qilsin (X o'rniga parametr). So'ngra salom_ber('Olim') ni print() orqali chiqaring.",
                    "expected_output": "Assalomu alaykum, Olim",
                    "ai_hints": "Matnlarni qo'shish + yoki f-string orqali qilinadi: return f'Assalomu alaykum, {ism}'"
                }
            ]
        },
        {
            "title": "6. Ma'lumotlar Tuzilmalari: Ro'yxatlar (List)",
            "content": """
            <h2>Ro'yxatlar bilan ishlash (Lists)</h2>
            <p>Biz bitta e'lon qilgan o'zgaruvchimizda butun boshli kolleksiyani (ko'plab ma'lumotlarni) saqlashimiz mumkin ekan! Eng ko'p tarqalgan ustun tur bu — `List` (Ro'yxat).</p>
            
            <div class="loop-demo" style="border: 2px solid var(--border); border-radius: 8px; padding: 10px; background: rgba(0,0,0,0.2);">
                <div class="loop-item" style="border-radius:4px; animation: none;">🍎</div>
                <div class="loop-item" style="border-radius:4px; animation: none;">🍌</div>
                <div class="loop-item" style="border-radius:4px; animation: none;">🍉</div>
            </div>

            <h3>Ro'yxat yaratish:</h3>
            <p>Ro'yxatlar doimo kvadrat qavslar <code>[ ]</code> ichiga, vergul bilan ajratilib yoziladi.</p>
            <pre><code>mevalar = ["olma", "banan", "gilos"]
raqamlar = [1, 5, 20, 100]</code></pre>
            
            <h3>Indekslash:</h3>
            <p>Ro'yxatning nolinchi (0) elementi bu uning boshlanishidir.</p>
            <pre><code>print(mevalar[0]) # "olma" chiqadi</code></pre>
            
            <div class="video-wrapper">
                <iframe src="https://www.youtube.com/embed/ohCDWZgNIU0" title="Python Lists" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
            </div>

            <h3>B’azi muhim metodlari:</h3>
            <ul>
                <li><code>.append(yangi)</code> — elementni ro'yxatning eng oxiriga qo'shadi.</li>
                <li><code>.pop()</code> — oxirgi elementni o'chiradi (yoki qaytaradi).</li>
                <li><code>len(ro'yxat)</code> — ro'yxatda nechta element borligini raqam qilib beradi.</li>
            </ul>
            """,
            "tasks": [
                {
                    "title": "Ro'yxatdagi uchinchi element",
                    "question": "ismlar = ['Anvar', 'Jasur', 'Malika', 'Dildora']. Shu ro'yxatdan 'Malika' ismini qavslar va indeks yordamida ekranga chiqaring.",
                    "expected_output": "Malika",
                    "ai_hints": "Ro'yxat 0 dan boshlanishini unutmang. 0-Anvar, 1-Jasur, 2-Malika..."
                },
                {
                    "title": "Yangi element qo'shish",
                    "question": "L = [10, 20, 30]. append metodidan foydalanib L ro'yxatiga 40 raqamini qo'shing va L ro'yxatini to'liqligicha print(L) orqali chiqaring.",
                    "expected_output": "[10, 20, 30, 40]",
                    "ai_hints": "L.append(40) orqali elementni ro'yxat so'ngiga qo'shasiz."
                },
                {
                    "title": "Yig'indisini hisoblash",
                    "question": "A = [1, 2, 3, 4, 5]. Uning barcha elementlari yig'indisini sum(A) o'rnatilgan funksiyasi yordamida ekranga chiqaring.",
                    "expected_output": "15",
                    "ai_hints": "Faqat print(sum(A)) deyishingiz kifoya."
                },
                {
                    "title": "Ro'yxat uzunligi",
                    "question": "B = ['a', 'b', 'c']. Bu yerdagi elementlar miqdorini len() funksiyasi orqali chop eting.",
                    "expected_output": "3",
                    "ai_hints": "len() ko'lamni qaytaradi: print(len(B))"
                }
            ]
        }
    ]

    for i, l_data in enumerate(lessons_data):
        lesson = Lesson.objects.create(
            course=course,
            title=l_data['title'],
            content=l_data['content'],
            order=i + 1
        )
        print(f"\nDars qo'shildi: {lesson.title}")
        
        for task_idx, t_data in enumerate(l_data['tasks']):
            Task.objects.create(
                lesson=lesson,
                title=t_data['title'],
                question=t_data['question'],
                expected_output=t_data['expected_output'],
                ai_hints=t_data.get('ai_hints', "")
            )
            print(f"  + Topshiriq qo'shildi: {t_data['title']}")

if __name__ == "__main__":
    populate()
    print("\n------------------------------")
    print("Muvaffaqiyatli yakunlandi! GIF lar CSS animatsiyalarga almashtirildi.")
    print("------------------------------")
