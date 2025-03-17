from django.urls import path
from .views import CreatePaypalPaymentView, ExecutePaypalPaymentView, CancelPaypalPaymentView, SavePaymentDetails, \
 RefundPaypalPaymentView

urlpatterns = [
    path('create/', CreatePaypalPaymentView.as_view(), name='paypal-create'),
    path('execute/', ExecutePaypalPaymentView.as_view(), name='paypal-execute'),
    path('cancel/', CancelPaypalPaymentView.as_view(), name='paypal-cancel'),
    path("save_details/", SavePaymentDetails.as_view(), name='save-details'),
    path("refund/", RefundPaypalPaymentView.as_view(), name='refund')
]

