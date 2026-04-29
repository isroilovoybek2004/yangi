import django, os, re, sys
sys.path.insert(0, r'C:\Users\Oybek\Desktop\diplom')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from lessons.models import Lesson
l = Lesson.objects.get(id=22)
print("TITLE:", l.title)
print("VIDEO_URL:", l.video_url)

# Content ichidagi barcha iframe src larini topish
iframes = re.findall(r'<iframe[^>]*src=["\']([^"\']+)["\'][^>]*>', l.content, re.IGNORECASE)
print("\nContent ichidagi iframe URLs:")
for i, src in enumerate(iframes):
    print(f"  {i+1}. {src}")

if not iframes:
    print("  (content ichida iframe yo'q)")
