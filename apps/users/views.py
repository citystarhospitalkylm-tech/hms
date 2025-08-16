from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, LoginSerializer
from .models import User
from django.shortcuts import render
from config.rbac import require_module

@require_module("users")
def users_dashboard(request):
    return render(request, "users/dashboard.html")

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens     = serializer.save()
        user_data  = UserSerializer(serializer.validated_data['user']).data
        return Response({**tokens, 'user': user_data}, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView):
    serializer_class    = UserSerializer
    permission_classes  = [IsAuthenticated]

    def get_object(self):
        return self.request.user