from django.contrib import admin
from .models import UserProfile, AccountPreference, Friendship, FriendRequestEvent, UserContentPermission
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AccountPreference)
admin.site.register(Friendship)
admin.site.register(FriendRequestEvent)
admin.site.register(UserContentPermission)
