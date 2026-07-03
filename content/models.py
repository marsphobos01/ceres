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
