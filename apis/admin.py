from django.contrib import admin
from .models import (
    CustomUser, Product, Order, Payment, Notification,
    PaymentGateway, SearchIndex, Location, VehicleCategory,
    OTPVerification, OrderOTP
)

# ✅ Register CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "mobile")
    search_fields = ("email", "mobile")

# ✅ Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_at")

# ✅ Order Admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "status", "total_price", "created_at")

# ✅ Notification Admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read", "created_at")
    search_fields = ("user__email", "message")

# ✅ Payment Admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "razorpay_order_id", "status")

# ✅ Register Remaining Models
admin.site.register(PaymentGateway)
admin.site.register(SearchIndex)
admin.site.register(Location)
admin.site.register(VehicleCategory)
admin.site.register(OTPVerification)
admin.site.register(OrderOTP)
