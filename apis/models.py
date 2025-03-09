from django.utils.timezone import now
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random

# ✅ Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, mobile, **extra_fields):
        if not mobile:
            raise ValueError("The mobile number must be set")
        user = self.model(mobile=mobile, **extra_fields)
        user.set_unusable_password()  # OTP ke bina login na ho
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(mobile, **extra_fields)

# ✅ Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)  # Optional Email
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "mobile"
    REQUIRED_FIELDS = ["email"]

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

    def __str__(self):
        return self.mobile

# ✅ Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    video = models.FileField(upload_to="product_videos/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now, editable=False)

    def __str__(self):
        return self.name

# ✅ Order Model
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("confirmed", "Confirmed"),
            ("shipped", "Shipped"),
            ("delivered", "Delivered"),
        ],
        default="pending",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

# ✅ Payment Model
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(
        max_length=20, choices=[("pending", "Pending"), ("success", "Success"), ("failed", "Failed")]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

# ✅ Payment Gateway Model
class PaymentGateway(models.Model):
    PAYMENT_METHODS = [
        ("razorpay", "Razorpay"),
        ("google_pay", "Google Pay"),
        ("paytm", "Paytm"),
        ("stripe", "Stripe"),
        ("upi", "UPI"),
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
        ("netbanking", "Net Banking"),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("success", "Success"), ("failed", "Failed")])
    created_at = models.DateTimeField(auto_now_add=True)

# ✅ Advanced Search Model
class SearchIndex(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    search_vector = SearchVectorField()

    def save(self, *args, **kwargs):
        self.search_vector = SearchVector("name", "description")  # Correct field names
        super().save(*args, **kwargs)

# ✅ Locations Model
class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="India")

# ✅ Vehicle Categories Model
class VehicleCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

# ✅ OTP Verification Model
class OTPVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# ✅ Order Confirmation via OTP Model
class OrderOTP(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

# ✅ Notification Model
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("email", "Email"),
        ("sms", "SMS"),
        ("whatsapp", "WhatsApp"),
        ("app", "In-App Notification"),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default="email")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.mobile if self.user else 'Guest'} - {self.notification_type} - {self.message[:30]}..."
