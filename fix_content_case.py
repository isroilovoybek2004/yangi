import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from lessons.models import Lesson
import re

for l in Lesson.objects.all():
    original_content = l.content
    new_content = l.content
    
    # Replace specifically identified strings
    new_content = new_content.replace("Birinchi Dasturingiz: 'Salom, Dunyo!'", "Birinchi dasturingiz: 'Salom, dunyo!'")
    new_content = new_content.replace("Birinchi Dasturingiz:", "Birinchi dasturingiz:")
    new_content = new_content.replace("'Salom, Dunyo!'", "'Salom, dunyo!'")
    new_content = new_content.replace("Hacking with Python", "Hacking with python") # Maybe?
    # Python is a proper noun, so "Hacking with Python" might be fine.
    # The user specifically highlighted "Avtomatlashtirish: Kundalik..." wait, "Avtomatlashtirish" is just the first word, so it's correct.
    # The red box highlights "Avtomatlashtirish: Kundalik zerikarli ishlarni kompyuterga topshirish." and "Birinchi Dasturingiz: 'Salom, Dunyo!'".
    # Wait, the red box is drawing attention to "Birinchi Dasturingiz: 'Salom, Dunyo!'".
    
    if new_content != original_content:
        l.content = new_content
        l.save()
        print(f"Updated content for Lesson: {l.title}")

print("Done")
