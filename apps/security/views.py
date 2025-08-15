from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
# security/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import RoleAuthenticationForm
ROLE_DASHBOARD = {
    'admin':    'admin:dashboard',
    'doctor':   'doctor:dashboard',
    'nurse':    'nurse:dashboard',
    'lab':      'labs:dashboard',
    'reception':'frontdesk:dashboard',
    'pharma':   'pharmacy:dashboard',
}

def login_view(request):
    if request.user.is_authenticated:
        return redirect(ROLE_DASHBOARD.get(request.user.role, 'home'))
    
    form = RoleAuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect(ROLE_DASHBOARD.get(user.role, 'home'))
    
    return render(request, 'security/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('security:login')


def login_view(request):
    form = RoleAuthenticationForm(request, data=request.POST or None)
    # … rest of  logic
def home(request):
    return HttpResponse("Hospital System is running. 🚀")

from .serializers import (
    UserSerializer,
    PasswordChangeSerializer,
    RoleSerializer,
    PermissionSerializer,
)

User = get_user_model()


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_205_RESET_CONTENT)


class PasswordChangeView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password updated successfully."}, status=status.HTTP_200_OK
        )


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = RoleSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer