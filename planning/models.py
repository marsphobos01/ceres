from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Q, F
from django.conf import settings
from academics.models import Module

# Create your models here.
class CalendarEvent(models.Model):
    class RecurrenceTypeChoices(models.TextChoices):
        NONE = "N", "None"
        DAILY = "D", "Daily"
        WEEKLY = "W", "Weekly"
        BIWEEKLY = "BW", "Biweekly"
        MONTHLY = "M", "Monthly"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    allday = models.BooleanField()
    colour = models.CharField(max_length=6, null=True, blank=True)
    location = models.CharField(max_length=100)
    recurrence_type = models.CharField(max_length=11, choices=RecurrenceTypeChoices.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(end__gt=F("start")),
                name='calendarevent_end_gt_start'
            )
        ]

class Task(models.Model):

    class PriorityChoices(models.TextChoices):
        HIGH = "H", "High"
        MEDIUM = "M", "Medium"
        LOW = "L", "Low"
        URGENT = "U", "Urgent"

    class StatusChoices(models.TextChoices):
        NOT_STARTED = "NS", "Not Started"
        IN_PROGRESS = "IP", "In Progress"
        COMPLETED = "CP", "Completed"
        CANCELED = "CN", "Canceled"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=100, choices=PriorityChoices.choices)
    status = models.CharField(max_length=100, choices=StatusChoices.choices)
    due_date = models.DateTimeField()
    parent_task = models.ForeignKey("self", on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_assignments')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_task_assignments', null=True, blank=True)
    assigned_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "user"],
                name="task_assignment_unique"
            )
        ]

class TaskLink(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='links')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    linked_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["task", "content_type", "object_id"],
                                    name="task_link_unique")

        ]




class StudySession(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='sessions', null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(end__gt=F("start")),
                name='studysession_end_gt_start'
            )]

class StudySessionsParticipant(models.Model):
    class ResponseChoices(models.TextChoices):
        INVITED = "I", "Invited"
        ACCEPTED = "A", "Accepted"
        DECLINED = "D", "Declined"


    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_session_participations')
    response = models.CharField(max_length=100, choices=ResponseChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "user"],
                name="unique_study_session_participant"
            )
        ]

class Deadline(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deadlines')
    title = models.CharField(max_length=100)
    due = models.DateTimeField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    links_to = GenericForeignKey('content_type', 'object_id')
    is_dismissed = models.BooleanField(default=False)
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
