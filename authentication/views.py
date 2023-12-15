from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from main.forms import SignUpForm
from django.contrib.auth.models import User


@csrf_exempt
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    print(username, password)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            # Status login sukses.
            is_staff = user.is_staff,
            return JsonResponse({
                "username": user.username,
                "is_staff": is_staff,
                "status": True,
                "message": "Login sukses!"
                # Tambahkan data lainnya jika ingin mengirim data ke Flutter.
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login gagal, akun dinonaktifkan."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login gagal, periksa kembali email atau kata sandi."
        }, status=401)


@csrf_exempt
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_confirm = request.POST.get('passwordConfirm')
    if request.method == "POST":
        if password_confirm == password:
            user = User.objects.create(username=username, password=password)
            user.save()
            return JsonResponse({
                "status": True,
                "message": "Register sukses!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Register gagal!"
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Register gagal!"
        }, status=401)


@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout berhasil!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout gagal."
        }, status=401)
