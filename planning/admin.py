from django.contrib import admin
from .models import CalendarEvent, Task, TaskAssignment, TaskLink, StudySession, StudySessionsParticipant, Deadline, TimetableImport

# Register your models here.
admin.site.register(CalendarEvent)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(TaskLink)
admin.site.register(StudySession)
admin.site.register(StudySessionsParticipant)
admin.site.register(Deadline)
admin.site.register(TimetableImport)
