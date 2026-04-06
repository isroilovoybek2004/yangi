from rest_framework import serializers
from lessons.models import Lesson, Task, Quiz, QuizQuestion, QuizChoice


class QuizChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = QuizChoice
        fields = ['id', 'choice_text', 'is_correct']


class QuizQuestionSerializer(serializers.ModelSerializer):
    choices = QuizChoiceSerializer(many=True, read_only=True)

    class Meta:
        model  = QuizQuestion
        fields = ['id', 'question_text', 'question_type', 'explanation', 'order', 'choices']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model  = Quiz
        fields = ['id', 'title', 'order', 'questions']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Task
        fields = [
            'id', 'lesson', 'title', 'question',
            'starter_code', 'expected_output', 'ai_hints',
            'difficulty', 'order',
        ]


class LessonSerializer(serializers.ModelSerializer):
    tasks   = TaskSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model  = Lesson
        fields = [
            'id', 'course', 'title', 'summary', 'content', 'order',
            'lesson_type', 'difficulty', 'estimated_minutes',
            'video_url', 'video_file', 'is_ai_generated',
            'tasks', 'quizzes',
        ]
