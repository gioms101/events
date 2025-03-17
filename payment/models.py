from django.contrib.auth.models import User
from django.db import models
from main.models import Movie


# Create your models here.
class PaymentTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255, unique=True)  # PayPal's payment ID (used for refunding)
    sale_id = models.CharField(max_length=255, null=True, blank=True)  # PayPal's sale ID (used for refunding)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)

