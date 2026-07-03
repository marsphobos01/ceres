from django.contrib import admin

from .models import (
    Assignment,
    AssignmentParticipant,
    Lecture,
    Module,
    ModuleMembership,
    RevisionTopic,
    TimetableEntry,
    TimetableImport,
)


class AssignmentParticipantInline(admin.TabularInline):
    model = AssignmentParticipant
    extra = 0


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    inlines = [AssignmentParticipantInline]


admin.site.register(Module)
admin.site.register(ModuleMembership)
admin.site.register(Lecture)
admin.site.register(TimetableEntry)
admin.site.register(AssignmentParticipant)
admin.site.register(RevisionTopic)
admin.site.register(TimetableImport)
