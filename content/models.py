from django.db import models
from django.conf import settings
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
