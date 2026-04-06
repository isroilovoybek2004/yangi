from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lessons.views import LessonViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
]
