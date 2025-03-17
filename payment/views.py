from django.urls import reverse
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import PPS
from .serializers import CreatePaymentSerializer, SavePaymentDetailsSerializer, RefundSerializer
from .models import PaymentTransaction
from .tasks import save_tickets, remove_user
from .permissions import CanBuyTicket


# Create your views here.

class CreatePaypalPaymentView(APIView):
    permission_classes = [IsAuthenticated, CanBuyTicket]
    serializer_class = CreatePaymentSerializer

    def post(self, request) -> Response:
        """
        total_amount should be evaluated by sending GET request to main/TotalPriceAPIView Endpoint

        :param request:
        :return: returns approval url in case of success else payment errors
        """
        total_amount = request.data.get('total_amount')

        return_url = request.build_absolute_uri(
            reverse('paypal-execute')
        )
        cancel_url = request.build_absolute_uri(
            reverse('paypal-cancel'))

        payment = PPS.create_payment(total_amount, return_url, cancel_url)
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return Response({"approval_url": link.href}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)


class ExecutePaypalPaymentView(APIView):
    serializer_class = None

    def get(self, request) -> Response:
        payment_id = request.query_params.get("paymentId")
        payer_id = request.query_params.get("PayerID")

        if not all([payment_id, payer_id]):
            return Response({"error": "Missing payment ID or Payer ID"}, status=status.HTTP_400_BAD_REQUEST)

        payment = PPS.execute_payment(payment_id, payer_id)
        if payment:
            return Response({"payment": payment.to_dict()}, status=status.HTTP_200_OK)
        else:
            return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)


class CancelPaypalPaymentView(APIView):
    serializer_class = None

    def get(self, request) -> Response:
        """
         PayPal Service sends GET request to that API ENDPOINT in case of canceling payment
        :param request:
        :return:
        """
        return Response({"message": "Payment cancelled"}, status=status.HTTP_200_OK)


class SavePaymentDetails(CreateAPIView):
    """
    This API endpoint should be requested after PayPal payment execution to save payment details safely
    """

    serializer_class = SavePaymentDetailsSerializer

    def perform_create(self, serializer):
        obj = serializer.save(user=self.request.user)
        save_tickets.delay(obj.event_id, obj.user_id)


class RefundPaypalPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RefundSerializer

    def post(self, request):
        payment_id = request.data.get("payment_id")
        if not payment_id:
            return Response({"error": "Payment ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = PaymentTransaction.objects.select_related('event').get(
                payment_id=payment_id,
            )
            self.check_object_permissions(self.request, transaction)
        except PaymentTransaction.DoesNotExist:
            return Response({"error": "Transaction not found."},
                            status=status.HTTP_404_NOT_FOUND)

        # Create a refund request using the sale_id
        refund = PPS.refund(transaction.sale_id, transaction.amount)

        if refund.success():
            remove_user.delay(transaction.event_id, transaction.user_id)
            return Response({"refund": refund.to_dict()}, status=status.HTTP_200_OK)
        else:
            return Response({"error": refund.error}, status=status.HTTP_400_BAD_REQUEST)
