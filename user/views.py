from rest_framework.generics import CreateAPIView
from .serializers import RegisterUserSerializer


class RegisterUserAPIView(CreateAPIView):
    serializer_class = RegisterUserSerializer
