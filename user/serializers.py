from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     validators=[validate_password],
                                     )

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "id")

