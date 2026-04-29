from rest_framework import viewsets, permissions
from lessons.models import Lesson, Task
from lessons.serializers import LessonSerializer, TaskSerializer

class LessonViewSet(viewsets.ModelViewSet):
    """ Darsliklar ro'yxati """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Lesson.objects.all()
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

class TaskViewSet(viewsets.ModelViewSet):
    """ Darsga tegishli topshiriqlar ro'yxati """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Task.objects.all()
        lesson_id = self.request.query_params.get('lesson')
        if lesson_id:
            queryset = queryset.filter(lesson_id=lesson_id)
        return queryset
