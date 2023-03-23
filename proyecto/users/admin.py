from django.contrib import admin
from .models import Profile,FriendRequest,Message,Match,Team,Tournament


admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(Match)
admin.site.register(Team)
admin.site.register(Tournament)
