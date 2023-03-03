from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils import timezone

REGIONCHOICES=[
        ('NA','NA'),
        ('EU','EU'),
        ('AP','AP'),
        ('KR','KR'),
]

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    def accept(self):
        self.accepted_at = timezone.now()
        self.save()

    def reject(self):
        self.delete()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    is_online = models.BooleanField(blank=True,default=False)
    looking_for_group = models.BooleanField(blank=True,default=False)

    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    valorantName = models.TextField(max_length=20, blank=True)
    valorantTagline = models.TextField(max_length=7, blank=True)
    valorantRegion = models.TextField(blank=True, choices=REGIONCHOICES)
    valorantLeague = models.TextField(max_length=40, blank=True)
    valorantRangue = models.TextField(max_length=40, blank=True)
    valorantCurrentRR = models.TextField(max_length=40, blank=True)
    valorantCalculatedElo = models.TextField(max_length=40, blank=True)
    valorantKills = models.TextField(max_length=40, blank=True)
    valorantDeaths = models.TextField(max_length=40, blank=True)
    valorantAssists = models.TextField(max_length=40, blank=True)
    valorantBodyshots = models.TextField(max_length=40, blank=True)
    valorantHeadshots = models.TextField(max_length=40, blank=True)
    friends = models.ManyToManyField(User, related_name='friends')
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    def get_absolute_url(self):
        print("entro¿¿")
        return "/"