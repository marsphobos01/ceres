from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class Note(models.Model):
    class Format(models.TextChoices):
        MARKDOWN = "markdown", "Markdown"
        RICH_TEXT = "rich_text", "Rich Text"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes')
    module = models.ForeignKey(
        'academics.Module', on_delete=models.CASCADE, related_name='notes', null=True, blank=True
    )
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    format = models.CharField(max_length=9, choices=Format.choices, default=Format.MARKDOWN)
    is_pinned = models.BooleanField(default=False)
    colour = models.CharField(max_length=6, null=True, blank=True)  # Hex colour code
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class NoteLink(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='note_links')
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["note", "content_type", "object_id"],
                                    name="note_link_unique"),
        ]

class Tag(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    colour = models.CharField(max_length=6, null=True, blank=True)  # Hex colour code
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="unique_tag_per_user"),
        ]

class TaggedContent(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tagged_contents')
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["tag", "content_type", "object_id"],
                                    name="tagged_content_unique"),
        ]

class Flashcard(models.Model):
    class Confidence(models.TextChoices):
        RED = 'red', 'Red'
        AMBER = 'amber', 'Amber'
        GREEN = 'green', 'Green'
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='flashcards')
    module = models.ForeignKey(
        'academics.Module', on_delete=models.CASCADE, related_name='flashcards', null=True, blank=True
    )
    deck = models.ForeignKey(
        'content.FlashcardDeck', on_delete=models.CASCADE, related_name='flashcards', null=True, blank=True
    )
    revision_topic = models.ForeignKey(
        'academics.RevisionTopic', on_delete=models.CASCADE, related_name='flashcards', null=True, blank=True
    )
    front = models.TextField()
    back = models.TextField()
    confidence = models.CharField(max_length=10, choices=Confidence.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FlashcardDeck(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='flashcard_decks')
    module = models.ForeignKey(
        'academics.Module', on_delete=models.CASCADE, related_name='flashcard_decks', null=True, blank=True
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NoteVersion(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["note", "version_number"], name="unique_note_version"),
        ]
