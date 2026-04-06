from rest_framework import viewsets, permissions
from lessons.models import Lesson, Task
from lessons.serializers import LessonSerializer, TaskSerializer

class LessonViewSet(viewsets.ModelViewSet):
    """ Darsliklar ro'yxati """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TaskViewSet(viewsets.ModelViewSet):
    """ Darsga tegishli topshiriqlar ro'yxati """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
