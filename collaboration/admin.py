from django.contrib import admin
from .models import StudyGroup, GroupMembership, GroupProject, GroupInvitation, ProjectMembership, DiscussionThread, DiscussionMessage, Conversation
# Register your models here.

admin.site.register(StudyGroup)
admin.site.register(GroupMembership)
admin.site.register(GroupProject)
admin.site.register(GroupInvitation)
admin.site.register(ProjectMembership)
admin.site.register(DiscussionThread)
admin.site.register(DiscussionMessage)
admin.site.register(Conversation)
