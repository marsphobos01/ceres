from django.contrib import admin
from .models import StudyGroup, GroupMembership
# Register your models here.

admin.site.register(StudyGroup)
admin.site.register(GroupMembership)
