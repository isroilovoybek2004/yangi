from django.db import migrations

def remove_course_suffix(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    for c in Course.objects.all():
        old_title = c.title
        c.title = c.title.replace(" (to'liq kurs)", '').replace(" (To'liq Kurs)", '').replace(' (toliq kurs)', '').strip()
        if old_title != c.title:
            c.save()

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_initial'),
    ]

    operations = [
        migrations.RunPython(remove_course_suffix),
    ]
