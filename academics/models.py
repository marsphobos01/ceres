from django.db import models
from django.conf import settings

# Create your models here.

class Module(models.Model):
    class Semester(models.TextChoices):
        AUTUMN = 'autumn', 'Autumn'
        SPRING = 'spring', 'Spring'
        SUMMER = 'summer', 'Summer'
        FULL_YEAR = 'full_year', 'Full Year'

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_modules'
    )
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    colour = models.CharField(max_length=6, null=True, blank=True)  # Hex colour code
    academic_year = models.CharField(max_length=9, null=True, blank=True)  # e.g., "2023/2024"
    semester = models.CharField(max_length=10, choices=Semester.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ModuleMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        MEMBER = 'member', 'Member'
        VIEWER = 'viewer', 'Viewer'
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='module_memberships'
    )
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MEMBER)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'module'], name='unique_user_module')
        ]
