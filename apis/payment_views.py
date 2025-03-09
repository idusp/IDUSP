# ✅ IMPORTS
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Order, Payment

# ✅ 1. Create Payment
@csrf_exempt
def create_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")

            order = Order.objects.get(id=order_id)
            amount = int(order.total_price * 100)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})

            Payment.objects.create(order=order, razorpay_order_id=payment["id"], status="created")

            return JsonResponse({"order_id": payment["id"], "amount": amount, "currency": "INR"}, status=201)

        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
