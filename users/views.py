from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Admin barcha foydalanuvchilarni ko'ra oladi, oddiy foydalanuvchi faqat o'zini
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(pk=self.request.user.pk)

    def get_permissions(self):
        # Yangi foydalanuvchi yaratish faqat admin orqali (register endpointi bor)
        if self.action == 'create':
            return [IsAdminUser()]
        return super().get_permissions()
