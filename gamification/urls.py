from django.urls import path
from gamification.views import (
    MyProfileView,
    LeaderboardView,
    MyBadgesView,
    MyStatsView,
)

urlpatterns = [
    # Foydalanuvchi o'z profili: XP, Level, Badge lar
    path('profile/',     MyProfileView.as_view(),   name='gamification-profile'),

    # Barcha badge lari va olingan vaqtlari
    path('badges/',      MyBadgesView.as_view(),    name='gamification-badges'),

    # To'liq statistika: submission soni, success rate, streak va h.k.
    path('stats/',       MyStatsView.as_view(),     name='gamification-stats'),

    # TOP-10 Leaderboard
    path('leaderboard/', LeaderboardView.as_view(), name='gamification-leaderboard'),
]
