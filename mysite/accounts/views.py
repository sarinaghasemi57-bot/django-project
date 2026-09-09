from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "این نام کاربری قبلاً وجود دارد"}
            )

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect("login")

    return render(request, "accounts/register.html")




def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("products")

    return render(request, "accounts/login.html")


def logout_user(request):
    logout(request)
    return redirect("products")