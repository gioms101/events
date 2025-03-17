import paypalrestsdk
from django.conf import settings


class PPS:
    @staticmethod
    def create_payment(amount, return_url, cancel_url):
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url
            },
            "transactions": [{
                "amount": {
                    "total": amount,
                    "currency": "USD"
                },
                "description": "Payment for your order"
            }]
        })
        return payment

    @staticmethod
    def execute_payment(payment_id, payer_id):
        payment = paypalrestsdk.Payment.find(payment_id)

        return payment if payment.execute({"payer_id": payer_id}) else None


    @staticmethod
    def refund(sale_id, amount):
        sale = paypalrestsdk.Sale.find(sale_id)
        refund = sale.refund({
            "amount": {
                "total": str(amount),
                "currency": "USD"
            }
        })
        return refund


paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # 'sandbox' or 'live'
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})
