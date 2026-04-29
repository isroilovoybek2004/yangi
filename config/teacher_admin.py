"""
O'qituvchi uchun maxsus Django AdminSite.
Faqat ta'lim tarkibiga oid bo'limlarni ko'rsatadi:
  - Courses
  - Lessons (Dars, Topshiriq, Quiz, Savollar)
"""
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _


# O'qituvchiga ko'rinadigan app va modellar
TEACHER_ALLOWED = {
    'courses':  ['course'],
    'lessons':  ['lesson', 'task', 'quiz', 'quizquestion', 'quizchoice'],
}


class TeacherAdminSite(AdminSite):
    site_header  = "PyLearn — O'qituvchi paneli"
    site_title   = "PyLearn Ustoz"
    index_title  = "Kurs va darslarni boshqarish"

    def has_permission(self, request):
        """
        Faqat is_staff bo'lgan, lekin is_superuser bo'lmagan foydalanuvchilar
        uchun bu panel ochiq.
        Superuser standart /admin/ ni ishlatadi.
        """
        return request.user.is_active and request.user.is_staff

    def get_app_list(self, request, app_label=None):
        """Faqat ruxsat etilgan app va modellarni qaytaradi."""
        full_list = super().get_app_list(request, app_label)
        filtered  = []
        for app in full_list:
            label    = app['app_label']
            allowed  = TEACHER_ALLOWED.get(label)
            if allowed is None:
                continue
            models = [
                m for m in app['models']
                if m['object_name'].lower() in allowed
            ]
            if models:
                app_copy          = dict(app)
                app_copy['models'] = models
                filtered.append(app_copy)
        return filtered


# Yagona instance — urls.py da import qilinadi
teacher_admin_site = TeacherAdminSite(name='teacher_admin')
