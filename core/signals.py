import secrets
from datetime import  timedelta

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from core.models import OtpToken

User = get_user_model()


@receiver(post_save, sender=User)
def send_opt_on_account_creation(sender,instance,created, **kwargs):
    if created:
        if instance.is_superuser:
            pass

        else:
            otp = secrets.token_hex(2).upper()
            OtpToken.objects.create(user=instance, otp=otp,expires=timezone.now() + timedelta(hours=1))

            send_mail(
                'Verify Account',
                f"Use this code {otp} to verify your account.",
                'noreply@example.com',  # Replace with your "from" email address
                [instance.email],
                fail_silently=False,
            )