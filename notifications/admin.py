from django.contrib import admin

from .models import Notification, Reminder, NotificationPreferences, NotificationDelivery, MutedContent

# Register your models here.
admin.site.register(Notification)
admin.site.register(Reminder)
admin.site.register(NotificationPreferences)
admin.site.register(NotificationDelivery)
admin.site.register(MutedContent)