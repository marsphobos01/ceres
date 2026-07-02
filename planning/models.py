from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q, F

# Create your models here.
class CalendarEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
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
                name='end_gte_start'
            )
        ]

class Task(models.Model):
    pass
class TaskAssignment(models.Model):
    pass
class TaskLink(models.Model):
    pass
class StudySession(models.Model):
    pass
class StudySessionsParticipant(models.Model):
    pass
class Deadline(models.Model):
    pass
class Goal(models.Model):
    pass