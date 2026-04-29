import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from progress.models import Progress, Submission

User = get_user_model()

teacher_group = Group.objects.get(name='Ustozlar')

models_to_view = [Progress, Submission, User]

for model in models_to_view:
    content_type = ContentType.objects.get_for_model(model)
    # Give view permissions for users and progress models
    # Ustoz shouldn't be able to delete/modify student progress or user profiles manually.
    perms = Permission.objects.filter(content_type=content_type, codename__startswith='view_')
    for perm in perms:
        teacher_group.permissions.add(perm)

print("Permissions updated for Ustozlar group.")
