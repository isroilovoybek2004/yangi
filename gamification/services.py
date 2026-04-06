from django.utils import timezone
from django.db import transaction
from gamification.models import UserProfile, Badge, UserBadge, calculate_level


class GamificationService:
    """
    Barcha gamification logikasi shu yerda.
    Submission, Progress va boshqa joylardan chaqiriladi.
    """

    # ─── XP miqdorlari ───────────────────────────────────────
    XP_CORRECT_SUBMISSION = 10   # To'g'ri javob uchun
    XP_FIRST_SUBMISSION   = 5    # Birinchi topshiriq uchun (bonus)

    @classmethod
    def get_or_create_profile(cls, user):
        """Foydalanuvchi profilini oladi yoki yangi yaratadi."""
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    @classmethod
    @transaction.atomic
    def award_xp(cls, user, amount: int, reason: str = ""):
        """
        Foydalanuvchiga XP beradi va leveli yangilanadi.
        Tranzaksiya ichida ishlaydi — xato bo'lsa hech narsa o'zgarmaydi.
        """
        profile = cls.get_or_create_profile(user)
        profile.xp += amount

        # Level avtomatik yangilanadi
        new_level, new_level_name = calculate_level(profile.xp)
        profile.level      = new_level
        profile.level_name = new_level_name

        # Streak yangilanadi (kunlik faollik)
        today = timezone.now().date()
        if profile.last_active_date:
            delta = (today - profile.last_active_date).days
            if delta == 1:
                profile.streak_days += 1   # Ketma-ket davom etyapti
            elif delta > 1:
                profile.streak_days = 1    # Streak uzildi, qaytadan boshlash
            # delta == 0: bugun allaqachon faol — streak o'zgarmaydi
        else:
            profile.streak_days = 1

        profile.last_active_date = today
        profile.save()
        return profile

    @classmethod
    def check_and_award_badges(cls, user):
        """
        Barcha badge shartlarini tekshiradi va layoqatlilarga beradi.
        Yangi badge topilsa — UserBadge yozuvi qo'shiladi.
        """
        from progress.models import Submission  # Circular import oldini olish
        profile        = cls.get_or_create_profile(user)
        already_earned = set(UserBadge.objects.filter(user=user).values_list('badge__code', flat=True))
        new_badges     = []

        def _give(badge_code):
            """Badge berish yordamchi funksiya."""
            if badge_code in already_earned:
                return
            try:
                badge = Badge.objects.get(code=badge_code)
                UserBadge.objects.get_or_create(user=user, badge=badge)
                new_badges.append(badge)
            except Badge.DoesNotExist:
                pass  # Badge katalogda yo'q — admindan qo'shilishi kerak

        # ── FIRST_STEP: Birinchi to'g'ri submission ──
        correct_count = Submission.objects.filter(user=user, is_correct=True).count()
        if correct_count >= 1:
            _give('FIRST_STEP')

        # ── ON_FIRE: 5 ta to'g'ri submission ──
        if correct_count >= 5:
            _give('ON_FIRE')

        # ── XP milestones ──
        if profile.xp >= 100:
            _give('XP_100')
        if profile.xp >= 500:
            _give('XP_500')
        if profile.xp >= 1000:
            _give('XP_1000')

        # ── COURSE_COMPLETE: Bir kursning barcha task larini bajargan ──
        from lessons.models import Task
        from courses.models import Course
        for course in Course.objects.all():
            tasks_in_course = Task.objects.filter(lesson__course=course)
            if tasks_in_course.exists():
                completed = Submission.objects.filter(
                    user=user,
                    task__in=tasks_in_course,
                    is_correct=True
                ).values('task').distinct().count()
                if completed >= tasks_in_course.count():
                    _give('COURSE_COMPLETE')
                    break  # Bitta kurs uchun yetarli

        return new_badges

    @classmethod
    def get_leaderboard(cls, limit=10):
        """XP bo'yicha saralangan TOP foydalanuvchilar ro'yxati."""
        return (
            UserProfile.objects
            .select_related('user')
            .order_by('-xp')[:limit]
        )

    @classmethod
    def get_user_stats(cls, user):
        """
        Foydalanuvchi uchun to'liq statistika.
        Dashboard va statistika sahifasida ishlatiladi.
        """
        from progress.models import Submission, Progress

        profile        = cls.get_or_create_profile(user)
        total_sub      = Submission.objects.filter(user=user).count()
        correct_sub    = Submission.objects.filter(user=user, is_correct=True).count()
        wrong_sub      = total_sub - correct_sub
        success_rate   = round((correct_sub / total_sub * 100), 1) if total_sub > 0 else 0.0
        completed_tasks= Progress.objects.filter(user=user, is_completed=True).count()
        badges_count   = UserBadge.objects.filter(user=user).count()

        # Keyingi level uchun qancha XP kerak
        from gamification.models import LEVEL_THRESHOLDS
        next_xp_needed = None
        for level, name, threshold in LEVEL_THRESHOLDS:
            if threshold > profile.xp:
                next_xp_needed = threshold - profile.xp
                break

        return {
            "xp":               profile.xp,
            "level":            profile.level,
            "level_name":       profile.level_name,
            "streak_days":      profile.streak_days,
            "next_xp_needed":   next_xp_needed,  # None = max levelda
            "total_submissions":  total_sub,
            "correct_submissions": correct_sub,
            "wrong_submissions":   wrong_sub,
            "success_rate":        success_rate,
            "completed_tasks":     completed_tasks,
            "badges_count":        badges_count,
        }
