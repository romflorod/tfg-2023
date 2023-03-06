from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(user_logged_out)
def set_user_offline(sender, user, request, **kwargs):
    request.user.profile.is_online=False
    request.user.save()