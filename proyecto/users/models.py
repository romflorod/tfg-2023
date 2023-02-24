from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

REGIONCHOICES=[
        ('NA','NA'),
        ('EU','EU'),
        ('AP','AP'),
        ('KR','KR'),
]
class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user")
    friends= models.ManyToManyField(User,blank=True,related_name="friends")
    def __str__(self):
        return self.user.username
    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()
    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()
    def unfriend(self,removee):
        #the removeer
        remover_friends_list= self 
        remover_friends_list.remove_friend(removee)
        friends_list=FriendList.objects.get(user=removee)
        friends_list.remove_friend(remover_friends_list.user)
        #removee removed by removeer
    def is_mutual_friend(self,friend):
        if friend in self.friends.all():
            return True
        else:
            return False
class FriendRequest(models.Model):
    #sender n receiver
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    is_active=models.BooleanField(blank=True,null=False,default=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        #acept the request
        receiver_friend_list=FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list=FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active= False
                self.save()

    def decline(self):
        self.is_active=False
        self.save()
    def cancel(self):
        self.is_active=False
        self.save()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    valorantName = models.TextField(max_length=20, blank=True)
    valorantTagline = models.TextField(max_length=3, blank=True)
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