from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import CustomUser, PaymentGateway
from .serializers import PaymentGatewaySerializer

# ✅ Home View
def home(request):
    return JsonResponse({"message": "Welcome to IDUSP API!"})

# ✅ Signup View
class SignupView(APIView):
    permission_classes = [AllowAny]  # Allow public access

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        mobile = request.data.get("mobile")

        # ✅ Error Handling
        if not username or not password or not email:
            return Response({"error": "Username, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ User Creation
        user = CustomUser.objects.create(
            username=username,
            email=email,
            mobile=mobile,
            password=make_password(password)  # Password securely hashed
        )
        return Response({"message": "Signup successful!", "user_id": user.id}, status=status.HTTP_201_CREATED)

# ✅ Payment Gateway View
class PaymentGatewayView(APIView):
    def get(self, request):
        """ Fetch all payment gateway transactions. """
        payments = PaymentGateway.objects.all()
        serializer = PaymentGatewaySerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """ Create a new payment gateway transaction. """
        serializer = PaymentGatewaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
