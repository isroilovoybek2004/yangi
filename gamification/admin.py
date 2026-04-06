from django.contrib import admin
from gamification.models import Badge, UserProfile, UserBadge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display  = ['icon', 'code', 'name', 'description']
    search_fields = ['name', 'code']
    list_display_links = ['code', 'name']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display  = ['user', 'xp', 'level', 'level_name', 'streak_days', 'last_active_date']
    search_fields = ['user__username']
    list_filter   = ['level']
    ordering      = ['-xp']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display  = ['user', 'badge', 'earned_at']
    search_fields = ['user__username', 'badge__name']
    list_filter   = ['badge']
    ordering      = ['-earned_at']
