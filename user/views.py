from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterUserSerializer, UserDetailSerializer


class RegisterUserAPIView(CreateAPIView):
    serializer_class = RegisterUserSerializer


class UserDetailsAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
