# ✅ IMPORTS
from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Product, Order, CustomUser
from .serializers import OrderSerializer

# ✅ 1. Create Order
@csrf_exempt
def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_id = data.get("user_id")
            product_id = data.get("product_id")
            quantity = int(data.get("quantity", 1))
            address = data.get("address")

            product = Product.objects.get(id=product_id)
            total_price = product.price * quantity
            estimated_time = now() + timedelta(hours=48)

            user = CustomUser.objects.get(id=user_id)

            order = Order.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                total_price=total_price,
                status='pending',
                address=address,
                estimated_delivery=estimated_time,
                payment_status=False
            )

            return JsonResponse({"message": "Order placed successfully!", "order_id": order.id}, status=201)

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        except CustomUser.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Only POST requests allowed"}, status=400)

# ✅ 2. Update Order Status
@csrf_exempt
def update_order_status(request, order_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status")

            if new_status not in ["pending", "confirmed", "shipped", "delivered"]:
                return JsonResponse({"error": "Invalid status"}, status=400)

            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()

            return JsonResponse({"message": "Order status updated successfully", "status": order.status})

        except Order.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
