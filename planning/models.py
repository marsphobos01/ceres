from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import Q, F
from django.conf import settings
#from academics.models import Module

# Create your models here.
class CalendarEvent(models.Model):
    class RecurrenceTypeChoices(models.TextChoices):
        NONE = "N", "None"
        DAILY = "D", "Dayly"
        WEEKLY = "W", "Weekly"
        BIWEEKLY = "BW", "Biweekly"
        MONTHLY = "M", "Monthly"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    allday = models.BooleanField()
    colour = models.CharField(max_length=6,  null=True)
    location = models.CharField(max_length=100)
    recurrence_type = models.CharField(max_length=11, choices=RecurrenceTypeChoices.choices, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end__gt=F("start")),
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
        COMPLETED = "CA", "Completed"
        CANCELED = "CD", "Canceled"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=100, choices=PriorityChoices.choices)
    status = models.CharField(max_length=100, choices=StatusChoices.choices)
    due_date = models.DateTimeField()
    parent_task = models.ForeignKey("self", on_delete=models.CASCADE, related_name='children', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

class TaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_assignment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_assigned_to_user')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_assigned_by_user', null=True)
    assigned_date = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "user"],
                name="task_assignment_unique"
            )
        ]

class TaskLink(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_link')
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
    #module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='sessions', null=True)
    title = models.CharField(max_length=100, null=True)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)
    location = models.CharField(max_length=100, null=True)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end__gt=F("start")),
                name='studysession_end_gt_start'
            )]

class StudySessionsParticipant(models.Model):
    class ResponceChoices(models.TextChoices):
        INVITED = "I", "Invited"
        ACCEPTED = "A", "Accepted"
        DECLINED = "D", "Declined"


    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='session_key')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant_user_key')
    response = models.CharField(max_length=100, choices=ResponceChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

class Deadline(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deadlines')
    title = models.CharField(max_length=100)
    due = models.DateTimeField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    links_to = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    is_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#TODO: after academics created uncomment import and module field in StudySession Model