
from django.db import models
from django.db.models import Q, F
from django.conf import settings

# Create your models here.
class CalendarEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=100)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    allday = models.BooleanField()
    location = models.CharField(max_length=100)
    recurrence = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end__gt=F("start")),
                name='calendarevent_end_gt_start'
            )
        ]

class Task(models.Model):
    PRIORITY_CHOICES = {"H": "High",
                        "L": "Low",
                        "C": "Critical"
                        }
    STATUS_CHOICES = {"P": "Pending",
                     "A": "Active",
                     "B": "Blocked",
                     "C": "Completed",
                     "AR": "Archived"}
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=100, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    progress = models.FloatField()
    due = models.DateTimeField()
    completed_timestamp = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(progress__lte=1) & models.Q(progress__gte=0),
                                   name='progress_bounds_check'),
        ]

class TaskAssignment(models.Model):
    ROLE_CHOICES = {} # TODO: decide on the role choices.
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_assignment')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_assigned_to')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_assigned_by')
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    assigned_date = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "assigned_to"],
                name="task_assignment_unique"
            )
        ]

class TaskLink(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_link')
    #app = TODO: write the link between the TaskLink and the "apps" table.

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["task", "app"],
    #         )
    #     ]



class StudySession(models.Model):
    SESSION_STATUS_CHOICES = {} #TODO: decide on the different status choices for study sessions.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    location = models.CharField(max_length=100)
    session_status = models.CharField(max_length=100, choices=SESSION_STATUS_CHOICES)
    note_summary = models.TextField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_time__gt=F("start_time")),
                name='studysession_end_gt_start'
            )]

class StudySessionsParticipant(models.Model):
    RESPONSE_CHOICES = {"I": "Invited",
                        "A": "Accepted",
                        "D": "Declined",
                        "AT": "Attended"
                        }
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='session_key')
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='participant_user_key')
    response = models.CharField(max_length=100, choices=RESPONSE_CHOICES)#
    invited_at = models.DateTimeField(null=True)
    responded_at = models.DateTimeField(null=True)#

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["session", "participant"],
                name="session_unique"
            )
        ]

class Deadline(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deadlines')
    title = models.CharField(max_length=100)
    due = models.DateTimeField()
    # source_app = TODO: write the link between the Deadline and the "apps" table.
    reminder = models.BooleanField(default=True)

class Goal(models.Model):
    GOAL_CHOICES = {} # TODO: Decide on the goal options.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=100)
    goal_type = models.CharField(max_length=100, choices=GOAL_CHOICES)
    target_value = models.FloatField()
    current_value = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gt=F("start_date")),
                name='goal_end_gt_start'
            ),
        models.CheckConstraint(condition=models.Q(target_value__lte=1) & models.Q(target_value__gte=0), name="target_value_bounds_check"),
            models.CheckConstraint(condition=models.Q(current_value__lte=1) & models.Q(current_value__gte=0), name="current_value_bounds_check"),
        ]
