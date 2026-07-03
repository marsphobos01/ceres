from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models


class Module(models.Model):
    class Semester(models.TextChoices):
        AUTUMN = "autumn", "Autumn"
        SPRING = "spring", "Spring"
        SUMMER = "summer", "Summer"
        FULL_YEAR = "full_year", "Full Year"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_modules",
    )
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    colour = models.CharField(max_length=6, null=True, blank=True)
    academic_year = models.CharField(max_length=9, null=True, blank=True)
    semester = models.CharField(
        max_length=10,
        choices=Semester.choices,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ModuleMembership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner", "Owner"
        MEMBER = "member", "Member"
        VIEWER = "viewer", "Viewer"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="module_memberships",
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "module"],
                name="unique_user_module",
            )
        ]


class Lecture(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="lectures",
    )
    title = models.CharField(max_length=255)
    date = models.DateTimeField(null=True, blank=True)
    room = models.CharField(max_length=100, null=True, blank=True)
    lecturer_name = models.CharField(max_length=255, null=True, blank=True)
    lecturer_email = models.EmailField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TimetableEntry(models.Model):
    class DayOfWeek(models.TextChoices):
        MONDAY = "mon", "Monday"
        TUESDAY = "tue", "Tuesday"
        WEDNESDAY = "wed", "Wednesday"
        THURSDAY = "thu", "Thursday"
        FRIDAY = "fri", "Friday"
        SATURDAY = "sat", "Saturday"
        SUNDAY = "sun", "Sunday"

    class RecurrenceType(models.TextChoices):
        WEEKLY = "weekly", "Weekly"
        FORTNIGHTLY = "fortnightly", "Fortnightly"
        ONE_OFF = "one_off", "One-off"

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="timetable_entries",
    )
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name="timetable_entries",
        null=True,
        blank=True,
    )
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=100, null=True, blank=True)
    recurrence_type = models.CharField(
        max_length=20,
        choices=RecurrenceType.choices,
        default=RecurrenceType.WEEKLY,
    )
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TimetableImport(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        COMPLETED = "completed", "Completed"
        COMPLETED_WITH_ERRORS = "completed_with_errors", "Completed with Errors"
        FAILED = "failed", "Failed"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="timetable_imports",
    )
    filename = models.CharField(max_length=100)
    status = models.CharField(
        max_length=21,
        choices=Status.choices,
        default=Status.PENDING,
    )
    total_rows = models.PositiveIntegerField(default=0)
    imported_rows = models.PositiveIntegerField(default=0)
    skipped_rows = models.PositiveIntegerField(default=0)
    error_rows = models.PositiveIntegerField(default=0)
    error_detail = models.JSONField(blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Assignment(models.Model):
    class SubmissionType(models.TextChoices):
        ESSAY = "essay", "Essay"
        REPORT = "report", "Report"
        PRESENTATION = "presentation", "Presentation"
        EXAM = "exam", "Exam"
        PRACTICAL = "practical", "Practical"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        NOT_SUBMITTED = "not_submitted", "Not Submitted"
        SUBMITTED = "submitted", "Submitted"

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    weighting = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )
    submission_type = models.CharField(
        max_length=20,
        choices=SubmissionType.choices,
        null=True,
        blank=True,
    )
    is_group = models.BooleanField(default=False)
    submission_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_SUBMITTED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="AssignmentParticipant",
        related_name="participating_assignments",
        blank=True,
    )

    def clean(self):
        super().clean()
        if self.pk and not self.is_group and self.participant_memberships.exists():
            raise ValidationError(
                {
                    "is_group": (
                        "Remove all assignment participants before changing this "
                        "assignment to individual work."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def can_manage_participants(self, user):
        if (
            not self.module_id
            or not getattr(user, "is_authenticated", False)
            or not getattr(user, "pk", None)
        ):
            return False

        if self.module.owner_id == user.pk:
            return True

        return ModuleMembership.objects.filter(
            module_id=self.module_id,
            user_id=user.pk,
            role=ModuleMembership.Role.OWNER,
        ).exists()

    def add_participant(self, *, actor, user):
        if not self.pk:
            raise ValueError("The assignment must be saved before adding participants.")
        if not self.can_manage_participants(actor):
            raise PermissionDenied(
                "Only the module owner or a module owner-member may manage participants."
            )
        return AssignmentParticipant.objects.create(assignment=self, user=user)

    def remove_participant(self, *, actor, user):
        if not self.can_manage_participants(actor):
            raise PermissionDenied(
                "Only the module owner or a module owner-member may manage participants."
            )
        return self.participant_memberships.filter(user=user).delete()


class AssignmentParticipantQuerySet(models.QuerySet):
    def bulk_create(self, objs, **kwargs):
        participant_rows = list(objs)
        for participant in participant_rows:
            participant.full_clean()
        return super().bulk_create(participant_rows, **kwargs)


class AssignmentParticipant(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="participant_memberships",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignment_participations",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AssignmentParticipantQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "user"],
                name="unique_assignment_participant",
            )
        ]

    def clean(self):
        super().clean()
        if not self.assignment_id or not self.user_id:
            return

        errors = {}
        assignment = self.assignment

        if not assignment.is_group:
            errors["assignment"] = (
                "Participants can only be added to group assignments."
            )

        has_module_access = (
            assignment.module.owner_id == self.user_id
            or ModuleMembership.objects.filter(
                module_id=assignment.module_id,
                user_id=self.user_id,
            ).exists()
        )
        if not has_module_access:
            errors["user"] = (
                "The participant must own or be a member of the assignment's module."
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class RevisionTopic(models.Model):
    class Confidence(models.TextChoices):
        RED = "red", "Red"
        AMBER = "amber", "Amber"
        GREEN = "green", "Green"

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="revision_topics",
    )
    title = models.CharField(max_length=255)
    confidence = models.CharField(
        max_length=10,
        choices=Confidence.choices,
        null=True,
        blank=True,
    )
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
