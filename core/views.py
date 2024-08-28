import secrets
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from core.models import OtpToken

User = get_user_model()


def index(request):
    print(request.user.is_authenticated)
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered.')
                return redirect(reverse('register'))

            username = email.split('@')[0]
            user = User.objects.create_user(email=email, password=password1, username=username)
            user.is_active = False
            user.save()

            # Generate OTP and save to OtpToken model
            otp = secrets.token_hex(2).upper()
            OtpToken.objects.create(user=user, otp=otp, expires=timezone.now() + timedelta(hours=1))

            send_mail(
                'Verify Account',
                f"Use this code {otp} to verify your account.",
                'noreply@example.com',  # Replace with your "from" email address
                [user.email],
                fail_silently=False,
            )

            request.session['email'] = email
            messages.success(request, 'Account created. Please check your email for OTP.')
            return redirect(reverse('enter_otp'))

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect(reverse('index'))
        messages.error(request, 'Invalid credentials.')
        return redirect(reverse('login'))
    return render(request, 'login.html')


def enter_otp(request):
    email = request.session.get('email')
    if not email:
        messages.error(request, 'Session expired. Please register again.')
        return redirect(reverse('register'))

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        messages.error(request, 'Invalid session. Please try again.')
        return redirect(reverse('register'))

    otp_user = OtpToken.objects.filter(user=user).last()

    if request.method == 'POST':
        otp = request.POST['otp']

        if otp_user.expires < timezone.now():
            messages.error(request, 'OTP expired.')
            return redirect(reverse('enter_otp'))

        if otp == otp_user.otp:
            user.is_active = True
            user.save()
            messages.success(request, 'Account verified. Please log in.')
            return redirect(reverse('login'))
        else:
            messages.error(request, 'Invalid OTP.')

    return render(request, 'opt.html')


def resend_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user with that email exists.')
            return redirect(reverse('resend_otp'))

        otp = secrets.token_hex(2).upper()
        OtpToken.objects.create(user=user, otp=otp, expires=timezone.now() + timedelta(hours=1))

        send_mail(
            'Verify Account',
            f"Use this code {otp} to verify your account.",
            'noreply@example.com',  # Replace with your "from" email address
            [user.email],
            fail_silently=False,
        )
        messages.success(request, 'OTP resent. Please check your email.')
        return redirect(reverse('enter_otp'))

    return render(request, 'send_opt.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect(reverse('index'))
