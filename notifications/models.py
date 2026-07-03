from django.db import models
from django.conf import settings



# Create your models here.
class CategoryChoices(models.TextChoices):
    # Current Vision — committed categories.
    ASSIGNMENT_REMINDER = "assignment_reminder", "Assignment Reminder",
    LECTURE_REMINDER = "lecture_reminder", "Lecture Reminder",
    CALENDAR_REMINDER = "calendar_reminder", "Calendar Reminder",
    GROUP_UPDATE = "group_update", "Group Update",
    FRIEND_REQUEST = "friend_request", "Friend Request",
    # Future/optional integrations — not yet committed scope.
    NEW_MESSAGE = "new_message", "New Message",
    STUDY_SESSION_INVITE = "study_session_invite", "Study Session Invite"


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_notifications")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_notifications", null=True, blank=True)
    category = models.CharField(choices=CategoryChoices.choices, max_length=25)
    title = models.CharField(max_length=120)
    body = models.TextField()
    source_app_label = models.CharField(max_length=120)
    source_object_type = models.CharField(max_length=120)
    source_object_id = models.PositiveIntegerField()
    read_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Reminder(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        CANCELED = "canceled", "Canceled"
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reminders")
    source_app_label = models.CharField(max_length=120)
    source_object_type = models.CharField(max_length=120)
    source_object_id = models.PositiveIntegerField()
    remind_at = models.DateTimeField()
    status = models.CharField(max_length=120, choices=StatusChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["recipient", "source_app_label", "source_object_type", "source_object_id", "remind_at"], name="unique_reminder")
        ]


class ChannelChoices(models.TextChoices):
    ALL = "all", "All",
    TEXT = "text", "Text",
    EMAIL = "emial",  "Email",
    DISCORD = "discord",  "Discord",
    IN_APP = "in_app",  "In App",



class NotificationPreferences(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    category = models.CharField(max_length=100, choices=CategoryChoices.choices)
    channel = models.CharField(max_length=100, choices=ChannelChoices.choices)
    enabled_flag = models.BooleanField(default=True)
    quiet_hours_start=models.TimeField()
    quiet_hours_end=models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "category", "channel"],
                #One preference per user per category per channel
                name="unique_notification_preferences"
            )
        ]


class NotificationDelivery(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        CANCELED = "canceled", "Canceled"
        SKIPPED = "skipped", "Skipped"
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='deliveries')
    channel = models.CharField(max_length=100, choices=ChannelChoices.choices)
    status = models.CharField(max_length=100, choices=StatusChoices.choices)
    attempted_at = models.DateTimeField(auto_now_add=True)
    provider_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["notification", "channel"], name="unique_notification_delivery")
        ]

class MutedContent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='muted_content')
    source_app_label = models.CharField(max_length=120)
    source_object_type = models.CharField(max_length=120)
    source_object_id = models.PositiveIntegerField()
    muted_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["user", "source_app_label", "source_object_type", "source_object_id"],
                name="unique_mute_per_user_and_source"
            )
        ]