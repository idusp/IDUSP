from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from apis.views import home, SendOTPView, VerifyOTPView

# ✅ Simple Home Page View
def home(request):
    return HttpResponse("<h1>Welcome to IDUSP E-Commerce!</h1>")

# ✅ Final URL Patterns (No Duplicates!)
urlpatterns = [
    path("admin/", admin.site.urls),  # 🔹 Django Admin Panel
    path("api/", include("apis.urls")),  # 🔹 API Routes
    path("", home, name="home"),  # 🔹 Home Page
]

# ✅ Static & Media Files (For Development Mode)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apis.urls')),  # Ensure the app's URLs are included
]
from django.contrib import admin
from django.urls import path, include
from apis.views import home, SendOTPView, VerifyOTPView  # ✅ Yaha import sahi karein

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/send-otp/', SendOTPView.as_view(), name='send_otp'),  # ✅ Class-based view me `.as_view()` zaroori hai
]
from django.contrib import admin
from django.urls import path, include
from apis.views import home  # Import the home view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apis.urls')),  # Ensure your API routes are included
    path('', home, name='home'),  # Add this line for the home page
]
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Tumhare baaki URLs yahan rahenge
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
