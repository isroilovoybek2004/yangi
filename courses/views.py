from rest_framework import viewsets, permissions
from courses.models import Course
from courses.serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    Kurslar ro'yxatini ko'rish va boshqarish.
    O'qish uchun hamma ruxsatga ega, yaratish/tahrirlash uchun faqat avtorizatsiyadan o'tganlar (yoki admin/instructor).
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
