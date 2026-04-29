import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from courses.models import Course
from lessons.models import Lesson, Task, Quiz, QuizQuestion, QuizChoice

User = get_user_model()

def setup_roles():
    print("Rollarni to'g'irlash...")

    # 1. Admin yaratish
    admin_user, created = User.objects.get_or_create(username='admin')
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print("Superuser 'admin' tayyor (parol: admin123).")


    # 2. Ustoz guruhini yaratish
    teacher_group, created = Group.objects.get_or_create(name='Ustozlar')
    
    # 3. Ruxsatlarni (permissions) berish
    # Ustoz boshqarishi mumkin bo'lgan modellar
    models_to_manage = [Course, Lesson, Task, Quiz, QuizQuestion, QuizChoice]
    
    for model in models_to_manage:
        content_type = ContentType.objects.get_for_model(model)
        permissions = Permission.objects.filter(content_type=content_type)
        for perm in permissions:
            teacher_group.permissions.add(perm)
            
    print("'Ustozlar' guruhi va huquqlari sozlandi.")

    # 4. testuser ni faqat ustoz qilish
    teacher_user, created = User.objects.get_or_create(username='testuser')
    teacher_user.set_password('password123')
    teacher_user.is_staff = True       # Admin panelga kirishi uchun
    teacher_user.is_superuser = False  # Superuser ekanligini olib tashlaymiz
    teacher_user.save()
    
    # Uni Ustozlar guruhiga qo'shamiz
    teacher_user.groups.add(teacher_group)
    print("'testuser' haqiqiy ustoz rolida (faqat o'quv jarayonini boshqaradi).")

if __name__ == '__main__':
    setup_roles()
