from django.contrib import admin
from .models import Module, ModuleMembership, Lecture,TimetableEntry, Assignment,RevisionTopic
# Register your models here.

admin.site.register(Module)
admin.site.register(ModuleMembership)
admin.site.register(Lecture)
admin.site.register(TimetableEntry)
admin.site.register(Assignment)
admin.site.register(RevisionTopic)
