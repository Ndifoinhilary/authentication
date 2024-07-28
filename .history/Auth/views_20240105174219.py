# pylint: disable=unused-argument
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Auth.forms import RegistrationForm
from Auth.models import User

# Create your views here.


def homePage(request):
    user = request.user
    return render(request, "home.html", {"user": user})


def registerUser(request):
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()

            if user is not None:
                login(request, user)
                return redirect("home")
        else:
            messages.error(request, "Invalid form check your data")
    return render(request, "register.html", {"form": form})


def loginUser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "Invalid form check your data")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

    return render(request, "login.html")


def logoutUser(request):
    logout(request)
    return redirect("home")
