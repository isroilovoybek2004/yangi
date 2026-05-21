from django.db import migrations
import re

def delete_first_lesson_video(apps, schema_editor):
    Lesson = apps.get_model('lessons', 'Lesson')
    # Bizga kerakli birinchi darsni sarlavhasi bo'yicha topamiz
    lessons = Lesson.objects.filter(title__icontains="Kirish va Python haqida tushuncha")
    for l in lessons:
        l.video_url = ""
        # Dars matni ichidagi video iframeni tozalaymiz
        old_content = l.content
        cleaned_content = re.sub(r'<div class="video-wrapper">.*?</div>', '', old_content, flags=re.DOTALL)
        cleaned_content = re.sub(r'<iframe .*?>.*?</iframe>', '', cleaned_content, flags=re.DOTALL)
        l.content = cleaned_content.strip()
        l.save()

class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_quiz_alter_lesson_options_alter_task_options_and_more'),
    ]

    operations = [
        migrations.RunPython(delete_first_lesson_video),
    ]
