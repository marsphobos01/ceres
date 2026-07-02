from django.contrib import admin
from .models import UserProfile, AccountPreference, Friendship, FriendRequestEvent, UserContentPermission, PrivacyPreference, FriendRequest, BlockedUser
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AccountPreference)
admin.site.register(Friendship)
admin.site.register(FriendRequestEvent)
admin.site.register(UserContentPermission)
admin.site.register(PrivacyPreference)
admin.site.register(FriendRequest)
admin.site.register(BlockedUser)
