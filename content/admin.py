from django.contrib import admin
from .models import Note, NoteLink, Tag, TaggedContent
# Register your models here.
admin.site.register(Note)
admin.site.register(NoteLink)
admin.site.register(Tag)
admin.site.register(TaggedContent)
