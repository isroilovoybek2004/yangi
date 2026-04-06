"""
Badge ma'lumotlarini ma'lumotlar bazasiga seed qiluvchi management command.
Ishlatish: python manage.py seed_badges
"""
from django.core.management.base import BaseCommand
from gamification.models import Badge


BADGES_DATA = [
    {
        'code': 'FIRST_STEP',
        'name': 'Birinchi qadam',
        'description': 'Birinchi topshiriqni muvaffaqiyatli bajardingiz!',
        'icon': '🏁',
    },
    {
        'code': 'ON_FIRE',
        'name': "Olovli o'rganuvchi",
        'description': "5 ta topshiriqni to'g'ri bajardingiz. Davom eting!",
        'icon': '🔥',
    },
    {
        'code': 'QUICK_THINKER',
        'name': 'Tez fikrlovchi',
        'description': "Topshiriqni tez va to'g'ri bajardingiz.",
        'icon': '⚡',
    },
    {
        'code': 'COURSE_COMPLETE',
        'name': 'Kursni tamomladi',
        'description': "Bitta kursning barcha topshiriqlarini bajardingiz!",
        'icon': '🎓',
    },
    {
        'code': 'TOP_LEARNER',
        'name': "Top o'rganuvchi",
        'description': "Leaderboardda TOP-3 ga kirdingiz!",
        'icon': '🏆',
    },
    {
        'code': 'XP_100',
        'name': '100 XP Yig\'dingiz',
        'description': "100 XP to'plash milestones'ini erishdingiz!",
        'icon': '💯',
    },
    {
        'code': 'XP_500',
        'name': '500 XP Yig\'dingiz',
        'description': "500 XP to'plash milestones'ini erishdingiz!",
        'icon': '🌟',
    },
    {
        'code': 'XP_1000',
        'name': 'Expert darajasi',
        'description': "1000 XP to'plab Expert darajasiga erishdingiz!",
        'icon': '🚀',
    },
]


class Command(BaseCommand):
    help = "Gamification badge ma'lumotlarini ma'lumotlar bazasiga qo'shadi."

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for badge_data in BADGES_DATA:
            badge, created = Badge.objects.update_or_create(
                code=badge_data['code'],
                defaults={
                    'name': badge_data['name'],
                    'description': badge_data['description'],
                    'icon': badge_data['icon'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"[YARATILDI] Badge: {badge.name}"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"[YANGILANDI] Badge: {badge.name}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"\nNatija: {created_count} ta yangi badge, {updated_count} ta mavjud yangilandi."
            )
        )
