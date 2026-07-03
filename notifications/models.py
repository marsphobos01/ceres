from django.db import models
from django.conf import settings



# Create your models here.
class CategoryChoices(models.TextChoices):
    ASSIGNMENT_REMIDER = "AR", "Assignment Reminder",
    LECTURE_REMINDER= "LR", "Lecture Reminder",
    CALENDAR_REMINDER= "CR", "Calendar Reminder",
    GROUP_UPDATE = "GU", "Group Update",
    FRIEDN_REQUEST = "FR", "Friend Request",
    NEW_MESSAGE = "NM", "New Message",
    STUDY_SESSION_INVITE = "SSI", "Study Session Invite"


class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_notifications")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_notifications", null=True, blank=True)
    category = models.CharField(choices=CategoryChoices.choices, max_length=3)
    title = models.CharField(max_length=120)
    body = models.TextField()
    source_app = models.CharField(max_length=120)
    source_object_type = models.CharField(max_length=120)
    source_object_id = models.PositiveIntegerField()
    read_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Reminder(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "P", "Pending"
        SENT = "S", "Sent"
        CANCELED = "C", "Canceled"
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
            models.UniqueConstraint(fields=["recipient", "source_app", "source_object_type", "source_object_id", "remind_at"], name="unique_reminder")
        ]


class ChannelChoices(models.TextChoices):
    ALL = "A", "All",
    TEXT = "T", "Text",
    EMAIL = "E",  "Email",
    DISCORD = "D",  "Discord",
    IN_APP = "I",  "In App",



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
        PENDING = "P", "Pending"
        SENT = "S", "Sent"
        CANCELED = "C", "Canceled"
        SKIPPED = "SK", "Skipped"
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
    source_app = models.CharField(max_length=120)
    source_object_type = models.CharField(max_length=120)
    source_object_id = models.PositiveIntegerField()
    muted_until = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["user", "source_app", "source_object_type", "source_object_id"],
                name="unique_mute_per_user_and_source"
            )
        ]