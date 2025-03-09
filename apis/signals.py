from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, Payment, Notification

# Order Confirmation Notification
@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):
    if created:  # New order created
        Notification.objects.create(
            recipient=instance.user,
            message_type="order_confirm",
            message=f"Your order {instance.id} has been placed successfully!"
        )

# Payment Confirmation Notification
@receiver(post_save, sender=Payment)
def payment_notification(sender, instance, created, **kwargs):
    if instance.status == "Paid":  # Payment confirmed
        Notification.objects.create(
            recipient=instance.order.user,
            message_type="payment_success",
            message=f"Your payment of ₹{instance.amount} for Order {instance.order.id} is successful!"
        )

# Delivery Notifications
@receiver(post_save, sender=Order)
def delivery_notification(sender, instance, **kwargs):
    if instance.status == "shipped":  # Order shipped
        Notification.objects.create(
            recipient=instance.user,
            message_type="delivery_update",
            message=f"Your order {instance.id} is out for delivery. Expected time: {instance.estimated_delivery}."
        )

    elif instance.status == "delivered":  # Order delivered
        Notification.objects.create(
            recipient=instance.user,
            message_type="post_delivery",
            message=f"Your order {instance.id} has been delivered! Thank you for shopping with us."
        )
