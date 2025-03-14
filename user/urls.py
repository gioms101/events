from django.urls import path
from .views import RegisterUserAPIView, UserDetailsAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path("user-detail/", UserDetailsAPIView.as_view(), name="details"),
]
