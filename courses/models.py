from django.db import models
from users.models import User

class Course(models.Model):
    """
    O'quv kurslari standarti (masalan: Python Asoslari, Django Backend).
    """
    title = models.CharField(max_length=255, verbose_name="Kurs nomi")
    description = models.TextField(blank=True, verbose_name="Kurs haqida")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses', verbose_name="O'qituvchi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
