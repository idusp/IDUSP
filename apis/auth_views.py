# ✅ IMPORTS
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import random

from .models import CustomUser

# ✅ 1. OTP Send
otp_storage = {}

def send_otp(request):
    mobile = request.GET.get("mobile")
    otp = random.randint(100000, 999999)
    otp_storage[mobile] = otp
    return JsonResponse({"message": f"OTP {otp} sent successfully!"})

# ✅ 2. OTP Verify
def verify_otp(request):
    mobile = request.GET.get("mobile")
    entered_otp = int(request.GET.get("otp", 0))
    if otp_storage.get(mobile) == entered_otp:
        user, created = CustomUser.objects.get_or_create(mobile=mobile)
        return JsonResponse({"message": "OTP verified!", "user_id": user.id})
    return JsonResponse({"message": "Invalid OTP"}, status=400)

# ✅ 3. Email & Password Login
@csrf_exempt
def email_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return JsonResponse({"message": "Login successful!", "user_id": user.id})
            return JsonResponse({"error": "Invalid credentials!"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests allowed"}, status=400)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random

User = get_user_model()

# 🔹 API 1: Send OTP
class SendOTPView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        if not mobile:
            return Response({"error": "Mobile number required"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(mobile=mobile)
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.save()

        # 🚀 Yahan SMS API se OTP send karo (Twilio ya Fast2SMS use kar sakte ho)
        print(f"OTP for {mobile}: {otp}")  # Testing ke liye

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)

# 🔹 API 2: Verify OTP & Login/Signup
class VerifyOTPView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')

        user = get_object_or_404(User, mobile=mobile)

        if user.otp == otp:
            user.otp = None  # OTP expire kar do
            user.save()
            return Response({"message": "Login successful", "user_id": user.id}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
