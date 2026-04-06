from rest_framework import authentication
from django.contrib.auth import get_user_model

User = get_user_model()

class DemoAuthentication(authentication.BaseAuthentication):
    """
    Ushbu klass orqali API so'rovlarni jo'natgan har qanday foydalanuvchi "Mehmon O'quvchi" bo'lib ko'rinadi.
    Tizimda login tizimi mutlaqo olib tashlanganligi sababli, progresslarni kuzatish uchun barcha 
    1 ta umumiy "Mehmon" foydalanuvchisiga yoziladi.
    """
    def authenticate(self, request):
        # Demo foydalanuvchi qidiriladi yoki yangi yaratiladi
        user, created = User.objects.get_or_create(
            username="Guest", 
            defaults={"email": "demo@example.com"}
        )
        if created:
            user.set_password("demo123456")
            user.save()
        
        # Har safar avtomatik ravishda tasdiqlangan (login bo'lgan) foydalanuvchi qaytariladi.
        return (user, None)
