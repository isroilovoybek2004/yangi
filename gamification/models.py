from django.db import models
from django.conf import settings


# ============================================================
# Level Tizimi — XP asosida hisoblash uchun konstantalar
# ============================================================
LEVEL_THRESHOLDS = [
    (1, "Yangi boshlovchi", 0),
    (2, "O'rganuvchi",      100),
    (3, "Bilimdon",         300),
    (4, "Ustoz",            600),
    (5, "Expert",           1000),
]


def calculate_level(xp):
    """XP asosida joriy level raqami va nomini qaytaradi."""
    current_level, current_name = 1, "Yangi boshlovchi"
    for level, name, threshold in LEVEL_THRESHOLDS:
        if xp >= threshold:
            current_level, current_name = level, name
    return current_level, current_name


# ============================================================
# Badge (Yutuqlar) Katalogi
# ============================================================
class Badge(models.Model):
    """
    Tizimda mavjud barcha yutuqlar (badge) lug'ati.
    Yangi badge qo'shish uchun shu modelga yozuv qo'shiladi.
    """
    BADGE_CHOICES = [
        ('FIRST_STEP',      '🏁 Birinchi qadam'),
        ('ON_FIRE',         '🔥 Olovli o\'rganuvchi'),
        ('QUICK_THINKER',   '⚡ Tez fikrlovchi'),
        ('COURSE_COMPLETE', '🎓 Kurs tamomladi'),
        ('TOP_LEARNER',     '🏆 Top o\'rganuvchi'),
        ('XP_100',          '💯 100 XP yig\'di'),
        ('XP_500',          '🌟 500 XP yig\'di'),
        ('XP_1000',         '🚀 Expert darajasi'),
    ]

    code        = models.CharField(max_length=50, unique=True, choices=BADGE_CHOICES, verbose_name="Kod")
    name        = models.CharField(max_length=100, verbose_name="Nomi")
    description = models.TextField(verbose_name="Tavsifi")
    icon        = models.CharField(max_length=10, default='🏅', verbose_name="Ikon (emoji)")
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.icon} {self.name}"

    class Meta:
        verbose_name = "Badge"
        verbose_name_plural = "Badge lar"


# ============================================================
# Foydalanuvchi Profili — XP va Level
# ============================================================
class UserProfile(models.Model):
    """
    Har bir foydalanuvchi uchun bitta profil.
    XP, Level va streak (ketma-ket faollik kunlari) saqlanadi.
    User model o'zgartirilmaydi — OneToOne orqali kengaytiriladi.
    """
    user            = models.OneToOneField(
                          settings.AUTH_USER_MODEL,
                          on_delete=models.CASCADE,
                          related_name='gamification_profile',
                          verbose_name="Foydalanuvchi"
                      )
    xp              = models.PositiveIntegerField(default=0, verbose_name="XP ball")
    level           = models.PositiveSmallIntegerField(default=1, verbose_name="Daraja")
    level_name      = models.CharField(max_length=50, default="Yangi boshlovchi", verbose_name="Daraja nomi")
    streak_days     = models.PositiveIntegerField(default=0, verbose_name="Ketma-ket kunlar")
    last_active_date= models.DateField(null=True, blank=True, verbose_name="Oxirgi faollik sanasi")
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} | Level {self.level} | {self.xp} XP"

    class Meta:
        verbose_name = "Foydalanuvchi profili"
        verbose_name_plural = "Foydalanuvchi profillari"


# ============================================================
# Foydalanuvchi Badge lari — kim qachon nima oldi
# ============================================================
class UserBadge(models.Model):
    """
    Foydalanuvchiga berilgan badge lar ro'yxati.
    Bir xil badge ikki marta berilmasligi uchun unique_together ishlatiladi.
    """
    user       = models.ForeignKey(
                     settings.AUTH_USER_MODEL,
                     on_delete=models.CASCADE,
                     related_name='badges',
                     verbose_name="Foydalanuvchi"
                 )
    badge      = models.ForeignKey(Badge, on_delete=models.CASCADE, verbose_name="Badge")
    earned_at  = models.DateTimeField(auto_now_add=True, verbose_name="Olingan vaqti")

    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-earned_at']
        verbose_name = "Foydalanuvchi Badge"
        verbose_name_plural = "Foydalanuvchi Badge lari"

    def __str__(self):
        return f"{self.user.username} → {self.badge.name}"


# ============================================================
# Kunlik Kirish Tarixi — heatmap uchun
# ============================================================
class DailyLogin(models.Model):
    """
    Foydalanuvchi qaysi kunlari platformaga kirganini kuzatadi.
    Heatmap diagrammasi uchun ishlatiladi.
    Bir kunda bir marta yoziladi (unique_together).
    """
    user = models.ForeignKey(
               settings.AUTH_USER_MODEL,
               on_delete=models.CASCADE,
               related_name='daily_logins',
               verbose_name="Foydalanuvchi"
           )
    date = models.DateField(verbose_name="Sana")

    class Meta:
        unique_together = ('user', 'date')
        ordering = ['-date']
        verbose_name = "Kunlik kirish"
        verbose_name_plural = "Kunlik kirishlar"

    def __str__(self):
        return f"{self.user.username} — {self.date}"
