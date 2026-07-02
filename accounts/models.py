from django.db import models
from django.conf import settings
from django.db.models import F, Q
from django.core.exceptions import ValidationError
from timezone_field import TimeZoneField
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AccountPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preference'
    )
    timezone = TimeZoneField(default='UTC')
    email_notifications = models.BooleanField(default=True)
    searchable = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Friendship(models.Model):
    user_one = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendships_as_user_one'
    )
    user_two = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendships_as_user_two'
    )
    status = models.CharField(max_length=255, choices=[
        ('accepted', 'Accepted'),
        ('removed', 'Removed'),
    ], default='accepted')
    accepted_at = models.DateTimeField(null=True, blank=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_one', 'user_two'], name='unique_friendship'
            ),
            models.CheckConstraint(
                condition=Q(user_one__lt=F('user_two')),
                name='user_one_before_user_two'
            ),
        ]

class FriendRequestEvent(models.Model):
    friendship = models.ForeignKey(Friendship, on_delete=models.CASCADE, related_name='events')
    actor_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_request_events')
    note = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()
        if self.actor_user not in [self.friendship.user_one, self.friendship.user_two]:
            raise ValidationError("Actor user must be one of the users involved in the friendship.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class UserContentPermission(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='content_permissions')
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='targeted_permissions')
    permission_level = models.CharField(max_length=255, choices=[
        ('view', 'View'),
        ('comment', 'Comment'),
        ('edit', 'Edit'),
    ])
    applies_to = models.CharField(max_length=255, choices=[
        ('all_content', 'All Content'),
        #('specific_content', 'Specific Content'),
    ])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner', 'target_user', 'applies_to'],
                name='unique_permission'
            ),
            models.CheckConstraint(
                condition=~Q(owner=F('target_user')),
                name='owner_not_target_user'
            ),
        ]


class PrivacyPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='privacy'
    )
    profile_visibility = models.CharField(max_length=255, choices=[
        ('public', 'Public'),
        ('friends_only', 'Friends Only'),
        ('private', 'Private'),
    ], default='private')
    show_online_status = models.BooleanField(default=True)
    allow_friend_requests = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=255, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['from_user', 'to_user'],
                condition=Q(status='pending'),
                name='unique_pending_friend_request'
            ),
            models.CheckConstraint(
                condition=~Q(from_user=F('to_user')),
                name='from_user_not_to_user'
            ),
        ]

class BlockedUser(models.Model):
    blocker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocked_users')
    blocked = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blocked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['blocker', 'blocked'],
                name='unique_blocked_user'
            ),
            models.CheckConstraint(
                condition=~Q(blocker=F('blocked')),
                name='no_self_blocking'
            ),
        ]
