from django.db import models
from django.conf import settings
from django.db.models import Q
# Create your models here.
class SearchIndexEntry(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLIC = "P",'PUBLIC'
        SHARED = "S",'SHARED'
        GROUP = "G", 'GROUP'
    source_app_label = models.CharField(max_length=100)
    source_object_type = models.CharField(max_length=100)
    source_object_id = models.PositiveIntegerField()
    title = models.TextField()
    summary = models.TextField()
    keywords = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='search_index_entries')
    visibility = models.CharField(max_length=100, choices=VisibilityChoices.choices)
    last_indexed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["source_app_label", "source_object_type", "source_object_id"],
                                    name="source_app_label_name_source_object_type_source_object_id"),
        ]

#class SearchAccessHint(models.Model):
#    class AccessLevelChoices(models.TextChoices):
#        VIEW = "view",'VIEW'
#        NONE = "none", 'NONE'
#    entry = models.ForeignKey(SearchIndexEntry, on_delete=models.CASCADE)
#    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#    access_level = models.CharField(max_length=4, choices=AccessLevelChoices.choices)
#    expires = models.DateTimeField(null=True)
#    created_at = models.DateTimeField(auto_now_add=True)

class SearchHistoryItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='search_history')
    query = models.TextField()
    filters = models.JSONField(blank=True, null=True)

    result_count = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class SavedSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=100)
    query = models.TextField()
    filters = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "name"],name="unique_user_to_name")
        ]


class SearchSynonym(models.Model):
    class ScopeChoices(models.TextChoices):
        GLOBAL = "global", "Global"
        ACADEMICS = "academics", "Academics"
        CONTENT = "content", "Content"
        FILES = "files", "Files"
        PLANNING = "planning", "Planning"
        ACCOUNTS = "accounts", "Accounts"
        COLLABORATION = "collaboration", "Collaboration"

    term = models.CharField(max_length=100)
    synonym = models.CharField(max_length=100)
    scope = models.CharField(max_length=100, choices=ScopeChoices.choices)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)#

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["term", "synonym"],
                    condition=Q(active=True),
                    name="unique_term"
            )
        ]
