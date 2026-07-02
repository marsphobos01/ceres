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
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    university = models.CharField(max_length=255, null=True, blank=True)
    course = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    visibility = models.CharField(max_length=255, choices=[
        ('public', 'Public'),
        ('friends','Friends'),
        ('private', 'Private'),
    ], default='private')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AccountPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='preference'
    )
    timezone = TimeZoneField(default='UTC')
    email_notifications = models.BooleanField(default=True)
    searchable = models.BooleanField(default=True)


class Friendship(models.Model):
    user_one = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendships_as_user_one'
    )
    user_two = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendships_as_user_two'
    )
    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friendship_requests_sent'
    )
    status = models.CharField(max_length=255, choices=[
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('blocked', 'Blocked'),
        ('removed', 'Removed'),
        ('rejected', 'Rejected'),
    ], default='requested')
    requested_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    removed_at = models.DateTimeField(null=True, blank=True)
    blocked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_one', 'user_two'], name='unique_friendship'
            ),
            models.CheckConstraint(
                condition= Q(requested_by=F('user_one')) | Q(requested_by=F('user_two')), name='requested_by_either_user'
            ),
            models.CheckConstraint(
                condition=Q(user_one__lt=F('user_two')),
                name='user_one_before_user_two'
            ),
        ]

class FriendRequestEvent(models.Model):
    friendship = models.ForeignKey(Friendship, on_delete=models.CASCADE, related_name='events')
    actor_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='friend_request_events')
    action = models.CharField(max_length=255, choices=[
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('removed', 'Removed'),
        ('blocked', 'Blocked'),
    ])
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
