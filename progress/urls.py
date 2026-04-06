from django.urls import path, include
from rest_framework.routers import DefaultRouter
from progress.views import ProgressViewSet, SubmissionViewSet, AIAssistView

router = DefaultRouter()
router.register(r'submissions', SubmissionViewSet, basename='submission')
router.register(r'', ProgressViewSet, basename='progress')

urlpatterns = [
    path('ai/<str:action_type>/', AIAssistView.as_view(), name='ai-assist'),
    path('', include(router.urls)),
]
