from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class StudyGroup(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class GroupMembership(models.Model):
    class Role(models.TextChoices):
        MEMBER = 'member', 'Member'
        OWNER = 'owner', 'Owner'
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INVITED = 'invited', 'Invited'
        LEFT = 'left', 'Left'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'study_group'], name='unique_membership')
        ]

class GroupProject(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE,null=True, blank=True)
    module = models.ForeignKey('academics.Module', on_delete=models.CASCADE,null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GroupInvitation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        DECLINED = 'declined', 'Declined'
        CANCELLED = 'cancelled', 'Cancelled'
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations')
    invited_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_invitations')
    study_group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE,null=True, blank=True)
    group_project = models.ForeignKey(GroupProject, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.study_group and self.group_project:
            raise ValidationError("Set either study_group or group_project, not both.")
        if not self.study_group and not self.group_project:
            raise ValidationError("Set either study_group or group_project.")


class ProjectMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        EDITOR = 'editor', 'Editor'
        VIEWER = 'viewer', 'Viewer'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_project = models.ForeignKey(GroupProject, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VIEWER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'group_project'], name='unique_project_membership')
        ]

class DiscussionThread(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

class DiscussionMessage(models.Model):
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Conversation(models.Model):
    class Type(models.TextChoices):
        DIRECT = 'direct', 'Direct'
        GROUP = 'group', 'Group'
    type = models.CharField(max_length=10, choices=Type.choices)
    created_at = models.DateTimeField(auto_now_add=True)

class ConversationParticipant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    muted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'conversation'], name='unique_conversation_participant')
        ]
