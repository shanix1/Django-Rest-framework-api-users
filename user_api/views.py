#views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotAllowed
from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, get_user_model
from django.contrib import messages

@api_view(['GET'])
def api_root(request):
    return Response({
        "register": "/api/register/",
        "token": "/api/token/",
        "users": "/api/users/"
    })

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

def login_view(request):
    return render(request, 'login.html')

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        cnic = request.POST.get('cnic')
        mobile = request.POST.get('mobile')
        profile_picture = request.FILES.get('profile_picture')

        # Validation
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('signup')

        if User.objects.filter(cnic=cnic).exists():
            messages.error(request, 'CNIC already registered.')
            return redirect('signup')

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            cnic=cnic,
            mobile=mobile,
            profile_picture=profile_picture
        )

        messages.success(request, 'User registered successfully!')
        return redirect('dashboard')

    return render(request, 'register.html')

@login_required
def dashboard_view(request):
    users = CustomUser.objects.all()
    return render(request, 'dashboard.html', {'users': users})

def logout_view(request):
    logout(request)
    return redirect('/login/')    

@csrf_exempt
def delete_user(request, pk):
    if request.method == 'POST':
        user = CustomUser.objects.get(pk=pk)
        user.delete()
        return redirect('/dashboard/')
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def update_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.cnic = request.POST.get('cnic')
        user.mobile = request.POST.get('mobile_number')  # ✔ Correct if form uses name="mobile_number"

        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES.get('profile_picture')

        user.save()
        return redirect('dashboard')
    return render(request, 'edit_user.html', {'user': user})

