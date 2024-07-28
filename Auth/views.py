# pylint: disable=unused-argument
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
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
            new_user = user.save()
            new_user = authenticate(
                request,
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            check = new_user is not None
            if check:
                login(request, user)
                return redirect("Auth:home")
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
        check = user is not None and user.check_password(password)
        if check:
            login(request, user)
            return redirect("Auth:home")

    return render(request, "login.html")


def logoutUser(request):
    logout(request)
    return redirect("Auth:home")
