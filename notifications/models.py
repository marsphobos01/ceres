from django.db import models
from django.conf import settings
# Create your models here.
CATEGORY_CHOICES = {"A": "Academic",
                        "C": "Colaboration"
                        }  # TODO: Refine the category choices.

class Notification(models.Model):
    notification_id = models.BigAutoField(primary_key=True)
    notification_name = models.CharField(max_length=100)
    notification_content = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True)
    #object_id = models.ForeignKey("Object", on_delete=models.CASCADE) # TODO: OneToOneField for the object model.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')

    """class Meta:
        constraints = [
            #TODO: Refine the category choices.
            models.CheckConstraint(
            check = models.Q(category__in=["A", "C"]),
            name="notification_category_valid"
            )
        ]"""


class Reminder(models.Model):
    STATUS_CHOICES = {"S": "Scheduled",
                      "ST": "Sent",
                      "C": "Canceled"
                      }
    FREQUENCY_CHOICES = {"O": "Once",
                        "RD": "Repeat Daily",
                         "RW": "Repeat Weekly",
                         "RB": "Repeat Biweekly",
                         "RM": "Repeat Monthly"
                        }
    reminder_id = models.BigAutoField(primary_key=True)
    reminder_content = models.TextField()
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,related_name='reminders')

    created_at = models.DateTimeField(auto_now_add=True)
    remind_at = models.DateTimeField()
    next_fire_at = models.DateTimeField(null=True)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default="O")
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="S")
    #object_id = models.ForeignKey("Object", on_delete=models.CASCADE) # TODO: OneToOneField for the object model.

    class Meta:
        constraints = [
            #TODO: add the reminder contratins, needs data that isn't written yet.
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