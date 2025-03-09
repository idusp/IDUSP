from django.urls import path
from . import views, auth_views, product_views, order_views, payment_views
from .auth_views import SendOTPView, VerifyOTPView

urlpatterns = [
    # 🔹 General APIs
    path("", views.home, name="home"),
    path("search/", views.search_products, name="search_products"),

    # 🔹 Authentication APIs
    path("auth/send-otp/", auth_views.send_otp, name="send_otp"),
    path("auth/verify-otp/", auth_views.verify_otp, name="verify_otp"),
    path("auth/login/", auth_views.email_login, name="email_login"),

    # 🔹 OTP-based Authentication (Class-based Views)
    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),

    # 🔹 Product APIs
    path("products/", product_views.ProductListView.as_view(), name="product_list"),
    path("products/add/", product_views.AddProductView.as_view(), name="add_product"),

    # 🔹 Order APIs
    path("orders/create/", order_views.create_order, name="create_order"),
    path("orders/update/<int:order_id>/", order_views.update_order_status, name="update_order_status"),

    # 🔹 Payment APIs
    path("payments/create/", payment_views.create_payment, name="create_payment"),
]

from django.urls import path
from .views import SendOTPView

urlpatterns = [
    path("send-otp/", SendOTPView.as_view(), name="send_otp"),
]
