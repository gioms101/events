from rest_framework import serializers
from .models import PaymentTransaction


class CreatePaymentSerializer(serializers.Serializer):
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ("payment_id",)


class SavePaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = ('event', "payment_id", "sale_id", 'amount')
