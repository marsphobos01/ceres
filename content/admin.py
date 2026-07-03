from django.contrib import admin
from .models import Note, NoteLink, Tag, TaggedContent, Flashcard, FlashcardDeck, NoteVersion, ContentCollection
# Register your models here.
admin.site.register(Note)
admin.site.register(NoteLink)
admin.site.register(Tag)
admin.site.register(TaggedContent)
admin.site.register(Flashcard)
admin.site.register(FlashcardDeck)
admin.site.register(NoteVersion)
admin.site.register(ContentCollection)
