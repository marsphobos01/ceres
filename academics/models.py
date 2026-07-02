from django.db import models
from django.conf import settings

# Create your models here.

class Module(models.Model):
    class Semester(models.TextChoices):
        AUTUMN = 'autumn', 'Autumn'
        SPRING = 'spring', 'Spring'
        SUMMER = 'summer', 'Summer'
        FULL_YEAR = 'full_year', 'Full Year'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_modules'
    )
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    colour = models.CharField(max_length=6, null=True, blank=True)  # Hex colour code
    academic_year = models.CharField(max_length=9, null=True, blank=True)  # e.g., "2023/2024"
    semester = models.CharField(max_length=10, choices=Semester.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ModuleMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        MEMBER = 'member', 'Member'
        VIEWER = 'viewer', 'Viewer'
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='module_memberships'
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'module'], name='unique_user_module')
        ]

class Lecture(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lectures')
    title = models.CharField(max_length=255)
    date = models.DateTimeField(null=True, blank=True)
    room = models.CharField(max_length=100, null=True, blank=True)
    lecturer_name = models.CharField(max_length=255, null=True, blank=True)
    lecturer_email = models.EmailField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TimetableEntry(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'

    class Recurrence(models.TextChoices):
        ONCE = 'once', 'once'
        DAILY = 'daily', 'Daily'
        WEEKLY = 'weekly', 'Weekly'
        FORTNIGHLY = 'fortnightly', 'Fortnightly'

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='timetable_entries')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='timetable_entries',null=True)
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100, null=True, blank=True)
    recurrence_type = models.CharField(max_length=20, choices=Recurrence.choices, default=Recurrence.ONCE)
    date = models.DateField(null=True, blank=True)  # For one-time events
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
