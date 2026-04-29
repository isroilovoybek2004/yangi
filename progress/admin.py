from django.contrib import admin
from .models import Progress, Submission

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'is_completed', 'score', 'completed_at')
    list_filter = ('is_completed', 'task__lesson__course')
    search_fields = ('user__username', 'task__title')
    readonly_fields = ('user', 'task', 'is_completed', 'score', 'ai_feedback')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'is_correct', 'timestamp')
    list_filter = ('is_correct', 'task__lesson__course')
    search_fields = ('user__username', 'task__title')
    readonly_fields = ('user', 'task', 'submitted_answer', 'is_correct', 'ai_feedback')
