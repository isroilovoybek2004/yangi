from rest_framework import serializers
from courses.models import Course
from users.serializers import UserSerializer

class CourseSerializer(serializers.ModelSerializer):
    instructor_detail = UserSerializer(source='instructor', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'instructor_detail', 'created_at']
