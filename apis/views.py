# ✅ IMPORTS
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.utils.timezone import now

from .models import Product, CustomUser
from .serializers import ProductSerializer

# ✅ 1. Home Page
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to IDUSP E-commerce!")

# ✅ 2. Search Products
def search_products(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
    ) if query else Product.objects.none()
    return render(request, 'search_results.html', {'results': results, 'query': query})

# ✅ 3. Verify OTP API
class VerifyOTPView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')

        user = get_object_or_404(CustomUser, mobile=mobile)

        # ✅ OTP Expiry Check (Assuming OTP expires in 5 minutes)
        if user.otp == otp and user.otp_created_at and now() - user.otp_created_at < timedelta(minutes=5):
            user.otp = None  # OTP expire
            user.otp_created_at = None
            user.save()
            return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SendOTPView(APIView):
    def get(self, request):  # ✅ Allow GET requests
        return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)

    def post(self, request):  # ✅ Allow POST requests
        return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)
