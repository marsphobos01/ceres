from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

# Create your models here.
class DashboardLayout(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    layout_name = models.CharField(max_length=120)
    widget_order = models.JSONField(default=dict)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DashboardWidget(models.Model):
    class DisplaySizeChoices(models.TextChoices):
        SMALL = "S", 'small'
        MEDIUM = "M", 'medium'
        LARGE = "L", 'large'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    widget_key = models.CharField(max_length=120,)
    enabled = models.BooleanField(default=True)
    display_size = models.CharField(max_length=120, choices=DisplaySizeChoices.choices)
    configuration = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'widget_key'],
                name='widget_key_unique'
            )
        ]


class QuickActionPreference(models.Model):
   user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   action_key = models.CharField(max_length=120)
   position = models.PositiveIntegerField()
   enabled = models.BooleanField(default=True)
   pinned = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   class Meta:
       constraints = [
           models.UniqueConstraint(
               fields=['user', 'action_key'],
               name='action_key_unique'
           ),
       ]


class UserInterfacePreference(models.Model):
    class ThemeChoices(models.TextChoices):
        LIGHT = 'L', 'light'
        DARK = 'D', 'dark'
        SYSTEM = 'S', 'system'
    class DensityChoices(models.TextChoices):
        COMPACT = 'CPT', 'compact'
        COMFORTABLE = 'CFE', 'comfortable'
        SPACE = 'SPC', 'spacious'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    theme = models.CharField(max_length=6, choices=ThemeChoices.choices)
    density = models.CharField(max_length=11, choices=DensityChoices.choices)
    sidebar_collapsed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)