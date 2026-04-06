from django.db import models
from courses.models import Course


class Lesson(models.Model):
    """
    Kurs ichidagi har bir dars/mavzu.
    """
    LESSON_TYPE_CHOICES = [
        ('theory', '📘 Nazariy dars'),
        ('video',  '🎬 Video dars'),
        ('mixed',  '🔀 Video + Matn'),
    ]
    DIFFICULTY_CHOICES = [
        ('beginner',     '🟢 Boshlang\'ich'),
        ('intermediate', '🟡 O\'rta'),
        ('advanced',     '🔴 Ilg\'or'),
    ]

    course             = models.ForeignKey(Course, on_delete=models.CASCADE,
                                           related_name='lessons',
                                           verbose_name="Kursga tegishli")
    title              = models.CharField(max_length=255, verbose_name="Dars mavzusi")
    summary            = models.CharField(max_length=500, blank=True,
                                           verbose_name="Qisqa tavsif")
    content            = models.TextField(blank=True, verbose_name="Dars matni (HTML)")
    order              = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    # Yangi maydonlar (mavjud data saqlanadi)
    lesson_type        = models.CharField(max_length=20, choices=LESSON_TYPE_CHOICES,
                                           default='theory', verbose_name="Dars turi")
    difficulty         = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES,
                                           default='beginner', verbose_name="Daraja")
    estimated_minutes  = models.PositiveIntegerField(default=5,
                                                      verbose_name="Taxminiy o'qish (daqiqa)")
    video_url          = models.URLField(blank=True, null=True,
                                          verbose_name="YouTube video URL")
    video_file         = models.FileField(upload_to='lessons/videos/', blank=True, null=True,
                                           verbose_name="Video fayl (upload)")
    is_ai_generated    = models.BooleanField(default=False,
                                              verbose_name="AI tomonidan yaratilganmi?")

    class Meta:
        ordering = ['order']
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.course.title} — {self.title}"


class Task(models.Model):
    """
    Darsga tegishli interaktiv kod topshirig'i.
    """
    DIFFICULTY_CHOICES = [
        ('beginner',     '🟢 Boshlang\'ich'),
        ('intermediate', '🟡 O\'rta'),
        ('advanced',     '🔴 Ilg\'or'),
    ]

    lesson          = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                                         related_name='tasks',
                                         verbose_name="Topshiriq darsi")
    title           = models.CharField(max_length=255, default="Vazifa",
                                        verbose_name="Topshiriq nomi")
    question        = models.TextField(verbose_name="Topshiriq sharti")
    starter_code    = models.TextField(blank=True,
                                        verbose_name="Boshlang'ich kod (foydalanuvchiga beriladi)")
    expected_output = models.TextField(verbose_name="Kutilayotgan natija")
    ai_hints        = models.TextField(blank=True, null=True,
                                        verbose_name="AI yordami / maslahat")
    difficulty      = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES,
                                        default='beginner', verbose_name="Daraja")
    order           = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order']
        verbose_name = "Kod topshirig'i"
        verbose_name_plural = "Kod topshiriqlari"

    def __str__(self):
        return f"💻 {self.title} ({self.lesson.title})"


# ─────────────────────────────────────────────────────────────
#  QUIZ / TEST MODELLARI
# ─────────────────────────────────────────────────────────────

class Quiz(models.Model):
    """
    Dars ichidagi test bloki.
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,
                                related_name='quizzes', verbose_name="Darsga tegishli")
    title  = models.CharField(max_length=255, verbose_name="Test nomi")
    order  = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order']
        verbose_name = "Test"
        verbose_name_plural = "Testlar"

    def __str__(self):
        return f"📝 {self.title} ({self.lesson.title})"


class QuizQuestion(models.Model):
    """
    Test ichidagi individual savol.
    """
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', '🔘 Ko\'p tanlov (A/B/C/D)'),
        ('true_false',      '✅ To\'g\'ri / Noto\'g\'ri'),
        ('code_output',     '💻 Kod natijasini toping'),
    ]

    quiz          = models.ForeignKey(Quiz, on_delete=models.CASCADE,
                                       related_name='questions', verbose_name="Testga tegishli")
    question_text = models.TextField(verbose_name="Savol matni")
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES,
                                      default='multiple_choice', verbose_name="Savol turi")
    explanation   = models.TextField(blank=True,
                                      verbose_name="To'g'ri javob izohi")
    order         = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")

    class Meta:
        ordering = ['order']
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"

    def __str__(self):
        return f"❓ {self.question_text[:60]}..."


class QuizChoice(models.Model):
    """
    Savol uchun javob varianti.
    """
    question    = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE,
                                     related_name='choices', verbose_name="Savolga tegishli")
    choice_text = models.CharField(max_length=500, verbose_name="Javob varianti matni")
    is_correct  = models.BooleanField(default=False, verbose_name="To'g'ri javobmi?")

    class Meta:
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"

    def __str__(self):
        icon = "✅" if self.is_correct else "❌"
        return f"{icon} {self.choice_text[:60]}"
