from django.db import models
from django.conf import settings



# Create your models here.
CATEGORY_CHOICES = {"AR": "Assignment Reminder",
                    "LR": "Lecture Reminder",
                    "CR": "Calendar Reminder",
                    "GU": "Group Update",
                    "FR": "Friend Request",
                    "NM": "New Message",
                    "SSI": "Study Session Invite"
                        }

class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="noticication_recipient_fk")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification_actor_fk")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=3)
    title = models.CharField(max_length=120)
    body = models.TextField()
    source_app = models.CharField(max_length=120)
    source_object_type = models.CharField(max_length=120)
    source_object_id = models.PositiveIntegerField()
    read_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Reminder(models.Model):
    STATUS_CHOICES = {"P": "Pending",
                      "S": "Sent",
                      "C": "Canceled",}
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reminder_recipient_fk")
    source_app = models.CharField(max_length=120)
    source_object_type = models.CharField(max_length=120)
    source_object_id = models.PositiveIntegerField()
    remind_at = models.DateTimeField()
    status = models.CharField(max_length=120, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["recipient", "source_app", "source_object_type", "source_object_id", "remind_at"], name="unique_reminder")
        ]


CHANNEL_CHOICES = {"A": "All",
                    "T":"Text",
                   "E": "Email",
                   "D": "Discord",
                   "I": "In App",
                   }


class NotificationPreferences(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    channel = models.CharField(max_length=100, choices=CHANNEL_CHOICES)
    enabled_flag = models.BooleanField(default=True)
    quiet_hours_start=models.TimeField()
    quiet_hours_end=models.TimeField()


class NotificationDelivery(models.Model):
    DELIVERY_STATUS_CHOICES = {"P": "Pending",
                               "S": "Sent",
                               "F":"Failed",
                               "SK": "Skipped"
                               }
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='delivery')
    channel = models.CharField(max_length=100, choices=CHANNEL_CHOICES)
    delivery_status = models.CharField(max_length=100, choices=DELIVERY_STATUS_CHOICES)
    attempted_at = models.DateTimeField(auto_now_add=True)
    provider_response = models.TextField()

class MutedContent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='muted_content')
    #source = models.ForeignKye("", on_delete=models.CASCADE, related_name="source") #TODO: Not written yet.
    muted_until = models.DateTimeField()

    """class Meta:

        constraints = [
            #TODO: Field not written yet.
            models.UniqueConstraint(
                fields=["user", "source"],
                name="unique_mute_per_user_and_source"
            )
        ]"""