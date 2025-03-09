import razorpay
import logging
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from .models import Order, Payment, Product, CustomUser

# Logging setup
logger = logging.getLogger(__name__)

def get_razorpay_client():
    """Lazy Initialization: Har request par Razorpay client initialize karein"""
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def create_razorpay_order(order):
    """
    Razorpay Order Create karne ka function
    """
    try:
        client = get_razorpay_client()
        amount = int(order.total_price * 100)  # Convert to paisa
        payment = client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})

        # Payment record save karein
        Payment.objects.create(order=order, razorpay_order_id=payment["id"], status="created")

        return payment
    except Exception as e:
        logger.error(f"Razorpay order creation failed: {str(e)}")
        return {"error": "Failed to create Razorpay order. Please try again later."}

def verify_razorpay_payment(data):
    """
    Razorpay Payment Verify karne ka function
    """
    try:
        client = get_razorpay_client()
        is_valid = client.utility.verify_payment_signature(data)

        if is_valid:
            payment = Payment.objects.get(razorpay_order_id=data["razorpay_order_id"])
            payment.status = "paid"
            payment.razorpay_payment_id = data["razorpay_payment_id"]
            payment.save()

            order = payment.order
            order.payment_status = True
            order.status = "confirmed"
            order.save()

            return {"message": "Payment Verified Successfully"}

        return {"error": "Invalid Signature"}
    
    except ObjectDoesNotExist:
        return {"error": "Payment record not found"}
    
    except Exception as e:
        logger.error(f"Payment verification failed: {str(e)}")
        return {"error": "Payment verification failed. Please try again later."}

def create_order_service(user_id, product_id, quantity, address):
    """
    Order Create karne ka function
    """
    try:
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

        return {"success": True, "order_id": order.id}

    except Product.DoesNotExist:
        return {"error": "Product not found"}
    
    except CustomUser.DoesNotExist:
        return {"error": "User not found"}
    
    except Exception as e:
        logger.error(f"Order creation failed: {str(e)}")
        return {"error": "Failed to create order. Please try again later."}
