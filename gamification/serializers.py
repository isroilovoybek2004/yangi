from rest_framework import serializers
from gamification.models import UserProfile, Badge, UserBadge


class BadgeSerializer(serializers.ModelSerializer):
    """Badge katalog ma'lumotlari."""
    class Meta:
        model  = Badge
        fields = ['id', 'code', 'name', 'description', 'icon']


class UserBadgeSerializer(serializers.ModelSerializer):
    """Foydalanuvchiga berilgan badge — badge detali bilan."""
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model  = UserBadge
        fields = ['badge', 'earned_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchi profili — XP, Level, Badge lari bilan.
    /api/gamification/profile/ da ishlatiladi.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    badges   = serializers.SerializerMethodField()

    class Meta:
        model  = UserProfile
        fields = [
            'username', 'xp', 'level', 'level_name',
            'streak_days', 'last_active_date', 'badges'
        ]

    def get_badges(self, obj):
        user_badges = UserBadge.objects.filter(user=obj.user).select_related('badge')
        return UserBadgeSerializer(user_badges, many=True).data


class LeaderboardSerializer(serializers.ModelSerializer):
    """
    Leaderboard ro'yxati uchun — umumiy ma'lumotlar.
    /api/gamification/leaderboard/ da ishlatiladi.
    """
    username    = serializers.CharField(source='user.username', read_only=True)
    badges_count = serializers.SerializerMethodField()

    class Meta:
        model  = UserProfile
        fields = ['username', 'xp', 'level', 'level_name', 'streak_days', 'badges_count']

    def get_badges_count(self, obj):
        return UserBadge.objects.filter(user=obj.user).count()


class UserStatsSerializer(serializers.Serializer):
    """
    To'liq statistika uchun serializer.
    /api/gamification/stats/ da ishlatiladi.
    """
    xp                   = serializers.IntegerField()
    level                = serializers.IntegerField()
    level_name           = serializers.CharField()
    streak_days          = serializers.IntegerField()
    next_xp_needed       = serializers.IntegerField(allow_null=True)
    total_submissions    = serializers.IntegerField()
    correct_submissions  = serializers.IntegerField()
    wrong_submissions    = serializers.IntegerField()
    success_rate         = serializers.FloatField()
    completed_tasks      = serializers.IntegerField()
    badges_count         = serializers.IntegerField()
