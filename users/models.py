from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Platformadagi barcha foydalanuvchilar (talaba, o'qituvchi, admin) uchun maxsus model.
    Keyinchalik qo'shimcha maydonlar (role, bio, avatar) qo'shish uchun qulay.
    """
    pass
