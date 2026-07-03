from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from .models import (
    CategoryChoices,
    ChannelChoices,
    MutedContent,
    Notification,
    NotificationPreferences,
    Reminder,
)

User = get_user_model()


class CategoryChoicesTests(TestCase):
    """
    Covers notifications issue #5: CategoryChoices correctness.

    - every accepted category is usable by both Notification and NotificationPreferences
    - an unsupported category value is rejected by both
    - both models share the same enum
    - enum member names are correctly spelled, and stored values were preserved
      across the ASSIGNMENT_REMIDER -> ASSIGNMENT_REMINDER rename
    """

    UNSUPPORTED_CATEGORY = "not_a_real_category"

    @classmethod
    def setUpTestData(cls):
        cls.recipient = User.objects.create_user(username="recipient", password="test-pass-123")
        cls.actor = User.objects.create_user(username="actor", password="test-pass-123")

    def _build_notification(self, category):
        return Notification(
            recipient=self.recipient,
            actor=self.actor,
            category=category,
            title="Test notification",
            body="Test body",
            source_app_label="academics",
            source_object_type="Assignment",
            source_object_id=1,
        )

    def _build_preference(self, category):
        return NotificationPreferences(
            user=self.recipient,
            category=category,
            channel=ChannelChoices.IN_APP,
            quiet_hours_start="22:00",
            quiet_hours_end="07:00",
        )

    def test_every_category_choice_is_accepted_by_notification(self):
        for value, _label in CategoryChoices.choices:
            with self.subTest(category=value):
                notification = self._build_notification(value)
                # read_at is null=True but not blank=True, so it fails full_clean()'s
                # blank check on an unrelated field unless excluded here; this test is
                # only concerned with category validation.
                notification.full_clean(exclude=["read_at"])
                notification.save()
                self.assertEqual(notification.category, value)

    def test_every_category_choice_is_accepted_by_notification_preferences(self):
        for value, _label in CategoryChoices.choices:
            with self.subTest(category=value):
                preference = self._build_preference(value)
                preference.full_clean()  # should not raise
                preference.save()
                self.assertEqual(preference.category, value)

    def test_unsupported_category_is_rejected_by_notification(self):
        notification = self._build_notification(self.UNSUPPORTED_CATEGORY)
        with self.assertRaises(ValidationError) as ctx:
            notification.full_clean(exclude=["read_at"])
        self.assertIn("category", ctx.exception.message_dict)

    def test_unsupported_category_is_rejected_by_notification_preferences(self):
        preference = self._build_preference(self.UNSUPPORTED_CATEGORY)
        with self.assertRaises(ValidationError) as ctx:
            preference.full_clean()
        self.assertIn("category", ctx.exception.message_dict)

    def test_notification_and_preferences_share_the_same_category_enum(self):
        notification_choices = Notification._meta.get_field("category").choices
        preference_choices = NotificationPreferences._meta.get_field("category").choices
        self.assertEqual(notification_choices, preference_choices)
        self.assertEqual(list(notification_choices), list(CategoryChoices.choices))

    def test_category_enum_members_are_correctly_spelled(self):
        # The rename target exists...
        self.assertTrue(hasattr(CategoryChoices, "ASSIGNMENT_REMINDER"))
        # ...and the old misspelled name is gone.
        self.assertFalse(hasattr(CategoryChoices, "ASSIGNMENT_REMIDER"))
        # FRIEND_REQUEST was already correctly spelled; confirm it stayed that way.
        self.assertTrue(hasattr(CategoryChoices, "FRIEND_REQUEST"))
        self.assertFalse(hasattr(CategoryChoices, "FRIEDN_REQUEST"))

    def test_rename_did_not_change_stored_values(self):
        # Renaming ASSIGNMENT_REMIDER -> ASSIGNMENT_REMINDER must not change what's
        # already stored in the database for existing rows.
        self.assertEqual(CategoryChoices.ASSIGNMENT_REMINDER.value, "assignment_reminder")
        self.assertEqual(CategoryChoices.FRIEND_REQUEST.value, "friend_request")

    def test_current_vision_categories(self):
        current_vision = {
            CategoryChoices.ASSIGNMENT_REMINDER,
            CategoryChoices.LECTURE_REMINDER,
            CategoryChoices.CALENDAR_REMINDER,
            CategoryChoices.GROUP_UPDATE,
            CategoryChoices.FRIEND_REQUEST,
        }
        future_optional = {
            CategoryChoices.NEW_MESSAGE,
            CategoryChoices.STUDY_SESSION_INVITE,
        }
        all_categories = {member for member in CategoryChoices}
        # Every category is classified as either current-Vision or future/optional,
        # and the two groups don't overlap.
        self.assertEqual(current_vision | future_optional, all_categories)
        self.assertEqual(current_vision & future_optional, set())


class SourceReferenceConstraintTests(TestCase):
    """
    Covers notifications issue #6: source-reference field naming and the
    uniqueness constraints that depend on it.

    Before this issue's fix, Reminder.unique_reminder and
    MutedContent.unique_mute_per_user_and_source both referenced a field
    ("source_app") that didn't exist on either model (the real field was
    "source_app_label"), which raised models.E012 the moment a database-aware
    command ran (migrate/test) -- see notifications/Notifications Database
    implementation.md for the full history.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="reminder_user", password="test-pass-123")
        # Fixed reference timestamps, computed once, so two "duplicate" builder
        # calls in the same test actually produce identical values -- calling
        # timezone.now() fresh inside the builder defaults would give each
        # reminder/mute a distinct microsecond-precision timestamp and silently
        # defeat the duplicate-rejection tests below.
        cls.default_remind_at = timezone.now() + timedelta(days=1)
        cls.default_muted_until = timezone.now() + timedelta(days=7)

    def _build_reminder(self, **overrides):
        defaults = dict(
            recipient=self.user,
            source_app_label="planning",
            source_object_type="Task",
            source_object_id=1,
            remind_at=self.default_remind_at,
            status=Reminder.StatusChoices.PENDING,
        )
        defaults.update(overrides)
        return Reminder(**defaults)

    def _build_muted_content(self, **overrides):
        defaults = dict(
            user=self.user,
            source_app_label="collaboration",
            source_object_type="StudyGroup",
            source_object_id=1,
            muted_until=self.default_muted_until,
        )
        defaults.update(overrides)
        return MutedContent(**defaults)

    def test_reminder_constraint_references_real_fields(self):
        # Would raise FieldDoesNotExist before the #6 fix, since the constraint
        # referenced "source_app" instead of "source_app_label".
        constraint = Reminder._meta.constraints[0]
        for field_name in constraint.fields:
            Reminder._meta.get_field(field_name)

    def test_muted_content_constraint_references_real_fields(self):
        constraint = MutedContent._meta.constraints[0]
        for field_name in constraint.fields:
            MutedContent._meta.get_field(field_name)

    def test_duplicate_reminder_is_rejected(self):
        self._build_reminder().save()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self._build_reminder().save()

    def test_reminder_with_distinct_source_is_valid(self):
        self._build_reminder().save()
        self._build_reminder(source_object_id=2).save()
        self.assertEqual(Reminder.objects.count(), 2)

    def test_reminder_with_distinct_remind_at_is_valid(self):
        self._build_reminder().save()
        self._build_reminder(remind_at=self.default_remind_at + timedelta(days=1)).save()
        self.assertEqual(Reminder.objects.count(), 2)

    def test_duplicate_muted_content_is_rejected(self):
        self._build_muted_content().save()
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self._build_muted_content().save()

    def test_muted_content_with_distinct_source_is_valid(self):
        self._build_muted_content().save()
        self._build_muted_content(source_object_id=2).save()
        self.assertEqual(MutedContent.objects.count(), 2)
