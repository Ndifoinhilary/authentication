import secrets
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail

from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils import  timezone

from core.models import OtpToken

# Create your views here.

User = get_user_model()
def index(request):

    print(request.user.is_authenticated)

    return  render(request, 'home.html')



def register(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            user  = User.objects.filter(email=email)
            if user.exists():
                messages.error(request, 'Email already registered.')
                return redirect(reverse('register'))
            username = email.split('@')[0]
            user = User.objects.create_user(email=email, password=password1, username=username)
            user.is_active = False
            user.save()
            request.session['email'] = email
            messages.success(request, 'Account created.')
            return redirect(reverse('opt'))

    return  render(request, 'signup.html' )


def  login_view(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect(reverse('index'))
        messages.error(request, 'Invalid email or password.')
        return redirect(reverse('login'))
    return  render(request, 'login.html')




def enter_opt(request):
    email = request.session['email']


    user = User.objects.get(email=email)
    otp_user = OtpToken.objects.filter(user=user).last()


    if request.method == 'POST':
        otp = request.POST['opt']

        if otp_user.expires.time() < timezone.now().time():
            messages.error(request, 'OTP expired.')
            return redirect(reverse('enter_opt'))
        if otp == otp_user.otp:
            user.is_active = True
            user.save()
            return redirect(reverse('login'))
        else:
            messages.error(request, 'Invalid OTP.')


    return  render(request, 'opt.html')



def resend_opt(request):

    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email)
        if user.exists():
            user = User.objects.get(email=email)

            otp = secrets.token_hex(2).upper()
            OtpToken.objects.create(user=user, otp=otp, expires=timezone.now() + timedelta(hours=1))

            send_mail(
                'Verify Account',
                f"Use this code {otp} to verify your account.",
                'noreply@example.com',  # Replace with your "from" email address
                [user.email],
                fail_silently=False,
            )
            return redirect(reverse('opt'))
        messages.error(request, 'No user with that email exists.')
        return redirect(reverse('resend_opt'))

    return render(request, 'send_opt.html')

def logout_view(request):
    logout(request)
    return  redirect(reverse('index'))






