from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.db.models import FileField



# Create your models here.
class StoredFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stored_files')
    filename=models.CharField(max_length=255)
    file = FileField(upload_to='files')
    mime_type=models.CharField(max_length=255)
    size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FileVersion(models.Model):
    stored_file = models.ForeignKey(StoredFile, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField()
    file = models.FileField(upload_to='files')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stored_file', 'version_number'], name='unique_file_version')
        ]

class FileLink(models.Model):
    stored_file = models.ForeignKey(StoredFile, on_delete=models.CASCADE, related_name='links')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    linked_to = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stored_file', 'content_type', 'object_id'], name='unique_link')
        ]



class FileShare(models.Model):
    class PermissionChoices(models.TextChoices):
        VIEW = "view", 'VIEW'
        EDIT = "edit", 'EDIT'
        DOWNLOAD = "download", 'DOWNLOAD'
        DELETE = "delete", 'DELETE'
    stored_file = models.ForeignKey(StoredFile, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='file_shares')
    permission = models.CharField(max_length=255, choices=PermissionChoices.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stored_file', 'user'], name='unique_share')
        ]

class FileTag(models.Model):
    stored_file = models.ForeignKey(StoredFile, on_delete=models.CASCADE, related_name='file_tags')
    tag = models.ForeignKey("content.Tag", on_delete=models.CASCADE, related_name='file_tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['stored_file', 'tag'], name='unique_tag')
        ]
class FilePreview(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "pending", 'PENDING'
        GENERATED ="generated", 'GENERATED'
        FAILED = "failed", 'FAILED'
    stored_file = models.OneToOneField(StoredFile, on_delete=models.CASCADE, related_name='preview')
    preview_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=9, choices=StatusChoices.choices,default=StatusChoices.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
