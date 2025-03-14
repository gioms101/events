from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'events', views.EventModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('total-price/', views.TotalPriceAPIView.as_view(), name="total-price"),
]
