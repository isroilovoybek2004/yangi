from django.contrib import admin
from django.utils.html import format_html
from lessons.models import Lesson, Task, Quiz, QuizQuestion, QuizChoice


# ─────────────────────────────────────────────────────────────
#  INLINE CLASSLAR
# ─────────────────────────────────────────────────────────────

class TaskInline(admin.StackedInline):
    """Dars ichidagi kod topshiriqlari"""
    model       = Task
    extra       = 1
    classes     = ('collapse',)
    fields      = (
        ('title', 'difficulty', 'order'),
        'question',
        'starter_code',
        'expected_output',
        'ai_hints',
    )
    verbose_name        = "Kod topshirig'i"
    verbose_name_plural = "💻 Kod topshiriqlari"


class QuizChoiceInline(admin.TabularInline):
    """Savol ichidagi javob variantlari"""
    model   = QuizChoice
    extra   = 2
    fields  = ('choice_text', 'is_correct')
    verbose_name        = "Javob varianti"
    verbose_name_plural = "Javob variantlari"


class QuizQuestionInline(admin.StackedInline):
    """Test ichidagi savollar"""
    model   = QuizQuestion
    extra   = 1
    classes = ('collapse',)
    fields  = (
        ('question_type', 'order'),
        'question_text',
        'explanation',
    )
    show_change_link    = True
    verbose_name        = "Savol"
    verbose_name_plural = "Savollar"


class QuizInline(admin.StackedInline):
    """Dars ichidagi testlar"""
    model               = Quiz
    extra               = 0
    classes             = ('collapse',)
    fields              = ('title', 'order')
    show_change_link    = True
    verbose_name        = "Test"
    verbose_name_plural = "📝 Testlar"


# ─────────────────────────────────────────────────────────────
#  ASOSIY ADMIN CLASSLAR
# ─────────────────────────────────────────────────────────────

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display  = (
        'title', 'course', 'lesson_type_badge',
        'difficulty_badge', 'estimated_minutes', 'order'
    )
    list_filter   = ('lesson_type', 'difficulty', 'course', 'is_ai_generated')
    search_fields = ('title', 'summary', 'content')
    ordering      = ('course', 'order')
    inlines       = [TaskInline, QuizInline]

    fieldsets = (
        ('📋 Asosiy ma\'lumot', {
            'fields': (
                ('course', 'order'),
                'title',
                'summary',
                ('lesson_type', 'difficulty', 'estimated_minutes'),
                'is_ai_generated',
            )
        }),
        ('📝 Dars matni (HTML)', {
            'classes': ('collapse',),
            'fields': ('content',),
        }),
        ('🎬 Video', {
            'classes': ('collapse',),
            'fields': (('video_url', 'video_file'),),
            'description': 'YouTube linki YOKI fayl yuklang (ikkalasini ham qo\'ysa bo\'ladi).',
        }),
    )

    def lesson_type_badge(self, obj):
        colors = {
            'theory': '#3b82f6',
            'video':  '#8b5cf6',
            'mixed':  '#06b6d4',
        }
        color = colors.get(obj.lesson_type, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',
            color, obj.get_lesson_type_display()
        )
    lesson_type_badge.short_description = "Tur"

    def difficulty_badge(self, obj):
        colors = {
            'beginner':     '#22c55e',
            'intermediate': '#f59e0b',
            'advanced':     '#ef4444',
        }
        color = colors.get(obj.difficulty, '#6b7280')
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:12px;font-size:11px">{}</span>',
            color, obj.get_difficulty_display()
        )
    difficulty_badge.short_description = "Daraja"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display  = ('title', 'lesson', 'difficulty', 'order')
    list_filter   = ('difficulty', 'lesson__course')
    search_fields = ('title', 'question', 'expected_output')
    ordering      = ('lesson', 'order')

    fieldsets = (
        ('💻 Topshiriq', {
            'fields': (
                ('lesson', 'order'),
                ('title', 'difficulty'),
                'question',
            )
        }),
        ('Kod', {
            'fields': ('starter_code', 'expected_output'),
        }),
        ('🤖 AI yordami', {
            'classes': ('collapse',),
            'fields': ('ai_hints',),
        }),
    )


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display  = ('title', 'lesson', 'order', 'question_count')
    list_filter   = ('lesson__course', 'lesson__difficulty')
    search_fields = ('title',)
    ordering      = ('lesson', 'order')
    inlines       = [QuizQuestionInline]

    def question_count(self, obj):
        count = obj.questions.count()
        return format_html(
            '<span style="font-weight:bold;color:#3b82f6">{} ta savol</span>', count
        )
    question_count.short_description = "Savollar"


@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display  = ('short_question', 'quiz', 'question_type', 'order')
    list_filter   = ('question_type',)
    search_fields = ('question_text',)
    ordering      = ('quiz', 'order')
    inlines       = [QuizChoiceInline]

    def short_question(self, obj):
        return obj.question_text[:70] + ('...' if len(obj.question_text) > 70 else '')
    short_question.short_description = "Savol"
