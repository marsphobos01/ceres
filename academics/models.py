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
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TimetableEntry(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = 'mon', 'Monday'
        TUESDAY = 'tue', 'Tuesday'
        WEDNESDAY = 'wed', 'Wednesday'
        THURSDAY = 'thu', 'Thursday'
        FRIDAY = 'fri', 'Friday'
        SATURDAY = 'sat', 'Saturday'
        SUNDAY = 'sun', 'Sunday'

    class RecurrenceType(models.TextChoices):
        WEEKLY = 'weekly', 'Weekly'
        FORTNIGHTLY = 'fortnightly', 'Fortnightly'
        ONE_OFF = 'one_off', 'One-off'

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='timetable_entries')
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='timetable_entries',null=True,blank=True)
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100, null=True, blank=True)
    recurrence_type = models.CharField(max_length=20, choices=RecurrenceType.choices, default=RecurrenceType.WEEKLY)
    date = models.DateField(null=True, blank=True)  # For one-time events
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TimetableImport(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        COMPLETED_WITH_ERRORS = "completed_with_errors", "Completed with Errors"
        FAILED = "failed", "Failed"
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='timetable_imports')
    filename = models.CharField(max_length=100)
    status = models.CharField(max_length=21, choices=Status.choices,default=Status.PENDING)
    total_rows = models.PositiveIntegerField(default=0)
    imported_rows = models.PositiveIntegerField(default=0)
    skipped_rows = models.PositiveIntegerField(default=0)
    error_rows = models.PositiveIntegerField(default=0)
    error_detail = models.JSONField(blank=True,default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Assignment(models.Model):
    class SubmissionType(models.TextChoices):
        ESSAY = 'essay', 'Essay'
        REPORT = 'report', 'Report'
        PRESENTATION = 'presentation', 'Presentation'
        EXAM = 'exam', 'Exam'
        PRACTICAL = 'practical', 'Practical'
        OTHER = 'other', 'Other'

    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        IN_PROGRESS = 'in_progress', 'In Progress'
        SUBMITTED = 'submitted', 'Submitted'
        COMPLETED = 'completed', 'Completed'
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    weighting = models.DecimalField(max_digits=5,decimal_places=2,null=True, blank=True)  # Weighting as a percentage
    submission_type = models.CharField(max_length=20, choices=SubmissionType.choices,null=True, blank=True)
    is_group = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RevisionTopic(models.Model):
    class Confidence(models.TextChoices):
        RED = 'red', 'Red'
        AMBER = 'amber', 'Amber'
        GREEN = 'green', 'Green'

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='revision_topics')
    title = models.CharField(max_length=255)
    confidence = models.CharField(max_length=10, choices=Confidence.choices,null=True,blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
