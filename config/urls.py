"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.static import serve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from config.teacher_admin import teacher_admin_site
import os

FRONTEND_DIR = os.path.join(settings.BASE_DIR, 'frontend')

class CustomTokenObtainPairView(TokenObtainPairView):
    """Login bo'lganda DailyLogin yozuvini yaratadi."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            try:
                from gamification.models import DailyLogin
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.filter(username=request.data.get('username')).first()
                if user:
                    DailyLogin.objects.get_or_create(user=user, date=timezone.now().date())
            except Exception:
                pass
        return response

# O'qituvchi paneli uchun modellarni ro'yxatdan o'tkazish
from courses.models import Course
from lessons.models import Lesson, Task, Quiz, QuizQuestion
from courses.admin import CourseAdmin
from lessons.admin import LessonAdmin, TaskAdmin, QuizAdmin, QuizQuestionAdmin
teacher_admin_site.register(Course,       CourseAdmin)
teacher_admin_site.register(Lesson,       LessonAdmin)
teacher_admin_site.register(Task,         TaskAdmin)
teacher_admin_site.register(Quiz,         QuizAdmin)
teacher_admin_site.register(QuizQuestion, QuizQuestionAdmin)

urlpatterns = [
    path("admin/",  admin.site.urls),
    path("ustoz/",  teacher_admin_site.urls),   # O'qituvchi paneli

    # JWT Authentication Endpoints
    path("api/token/", CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),

    # App Endpoints
    path("api/users/", include("users.urls")),
    path("api/courses/", include("courses.urls")),
    path("api/lessons/", include("lessons.urls")),
    path("api/progress/", include("progress.urls")),
    path("api/gamification/", include("gamification.urls")),

    # Frontend static fayllarni serve qilish
    re_path(r'^frontend/(?P<path>.*)$', serve, {'document_root': FRONTEND_DIR}),

    # Root URL → frontend ga yo'naltirish
    path('', RedirectView.as_view(url='/frontend/index.html', permanent=False), name='home'),
]

# Development: media fayllarga kirish uchun
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
