from django.db import models
from users.models import User
from lessons.models import Task

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress', verbose_name="Talaba")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progress', verbose_name="Topshiriq")
    is_completed = models.BooleanField(default=False, verbose_name="Bajarildi")
    score = models.IntegerField(default=0, verbose_name="Bal")
    ai_feedback = models.TextField(blank=True, null=True, verbose_name="Eng so'nggi AI xulosasi")
    completed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'task')

    def __str__(self):
        status = 'Bajarildi' if self.is_completed else 'Jarayonda'
        return f"{self.user.username} | {self.task.title} | {status}"

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions', verbose_name="Talaba")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions', verbose_name="Topshiriq")
    submitted_answer = models.TextField(verbose_name="Yuborilgan javob/kod")
    is_correct = models.BooleanField(default=False, verbose_name="To'g'rimi?")
    ai_feedback = models.TextField(blank=True, null=True, verbose_name="Ushbu urinish uchun AI xulosasi")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.task.title} (To'g'ri: {self.is_correct})"
