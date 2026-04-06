from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from gamification.models import UserBadge
from gamification.serializers import (
    UserProfileSerializer,
    LeaderboardSerializer,
    UserBadgeSerializer,
    UserStatsSerializer,
)
from gamification.services import GamificationService


class MyProfileView(APIView):
    """
    Foydalanuvchi o'zining gamification profilini ko'radi.
    GET /api/gamification/profile/  →  XP, Level, Badge lar
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = GamificationService.get_or_create_profile(request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)


class LeaderboardView(APIView):
    """
    TOP-10 foydalanuvchilar XP bo'yicha.
    GET /api/gamification/leaderboard/
    Autentifikatsiya shart emas — hamma ko'ra oladi.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        queryset = GamificationService.get_leaderboard(limit=10)
        serializer = LeaderboardSerializer(queryset, many=True)
        return Response(serializer.data)


class MyBadgesView(APIView):
    """
    Foydalanuvchining barcha badge lari ro'yxati.
    GET /api/gamification/badges/  →  earned badge lar va sanalar
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_badges = (
            UserBadge.objects
            .filter(user=request.user)
            .select_related('badge')
            .order_by('-earned_at')
        )
        serializer = UserBadgeSerializer(user_badges, many=True)
        return Response(serializer.data)


class MyStatsView(APIView):
    """
    Foydalanuvchining to'liq statistikasi.
    GET /api/gamification/stats/ → submission statistikasi, XP, level,
                                    streak, badges soni va keyingi level chegarasi
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stats = GamificationService.get_user_stats(request.user)
        serializer = UserStatsSerializer(data=stats)
        serializer.is_valid()          # Serializer data bilan ishlaydi
        return Response(serializer.data)
