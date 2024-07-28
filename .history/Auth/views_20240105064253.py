# pylint: disable=unused-argument
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from Auth.forms import RegistrationForm

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

            messages.success(request, "Your account has been created successfully")

            if user is not None:
                login(request, user)
                return redirect("home")
        else:
            messages.error(request, "Check your credentials and try again")
    return render(request, "register.html", {"form": form})


def loginUser(request):
    return render(request, "login.html")


def logoutUser(request):
    pass
