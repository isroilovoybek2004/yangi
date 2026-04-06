from rest_framework import serializers
from progress.models import Progress, Submission
from users.serializers import UserSerializer
from lessons.serializers import TaskSerializer

class ProgressSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(source='user', read_only=True)
    task_detail = TaskSerializer(source='task', read_only=True)

    class Meta:
        model = Progress
        fields = ['id', 'user', 'user_detail', 'task', 'task_detail', 'is_completed', 'score', 'ai_feedback', 'completed_at']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'user', 'task', 'submitted_answer', 'is_correct', 'ai_feedback', 'timestamp']
        read_only_fields = ['user', 'is_correct', 'ai_feedback']
