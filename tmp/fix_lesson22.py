import django, os, re, sys
sys.path.insert(0, r'C:\Users\Oybek\Desktop\diplom')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from lessons.models import Lesson
l = Lesson.objects.get(id=22)

print("Avvalgi content ichidagi iframe:")
# AWek4Yv0Krs iframe ni topib o'chirish
old_content = l.content

# Butun iframe tegini (wrapper div bilan) o'chirish
# Pattern: <iframe ... AWek4Yv0Krs ... ></iframe> yoki <iframe ... />
new_content = re.sub(
    r'<iframe[^>]*AWek4Yv0Krs[^>]*>\s*</iframe>',
    '',
    old_content,
    flags=re.IGNORECASE | re.DOTALL
)
# Self-closing variant
new_content = re.sub(
    r'<iframe[^>]*AWek4Yv0Krs[^>]*/?>',
    '',
    new_content,
    flags=re.IGNORECASE | re.DOTALL
)

if new_content != old_content:
    l.content = new_content
    l.save()
    print("SUCCESS: iframe o'chirildi!")
    # Tekshirish
    remaining = re.findall(r'<iframe[^>]*src=["\']([^"\']+)["\'][^>]*>', new_content, re.IGNORECASE)
    print("Qolgan iframalar:", remaining if remaining else "yo'q")
else:
    print("WARN: iframe topilmadi, manual o'chirish kerak!")
    # Content ichidagi iframe qismini ko'rsatish
    found = re.findall(r'<iframe[^>]*>[^<]*</iframe>|<iframe[^>]*/>', old_content, re.IGNORECASE | re.DOTALL)
    for f in found:
        print("Topilgan iframe:", f[:200])
