from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from .models import Task, TaskRecurrence

User = get_user_model()


class RecurrenceConstraintTestCase(TestCase):
    """
    Shared fixtures and builders for the task-recurrence constraint tests.

    A TaskRecurrence must point at an existing template Task, so the
    recurrence builder creates a fresh (non-recurring) template task per
    call — the template_task OneToOneField forbids sharing one.
    """

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="planner", password="test-pass-123")
        # A single fixed reference time keeps the boundary comparisons between
        # starts_at / ends_at / next_occurrence_at exact; calling timezone.now()
        # inside the builders would make "equal" timestamps silently unequal.
        cls.starts_at = timezone.now()
        cls.day = timedelta(days=1)

    def _build_task(self, **overrides):
        defaults = dict(
            owner=self.owner,
            title="Task",
            description="A task",
            priority=Task.PriorityChoices.MEDIUM,
            status=Task.StatusChoices.NOT_STARTED,
            due_date=self.starts_at + self.day,
        )
        defaults.update(overrides)
        return Task(**defaults)

    def _create_task(self, **overrides):
        task = self._build_task(**overrides)
        task.save()
        return task

    def _build_recurrence(self, **overrides):
        defaults = dict(
            frequency=TaskRecurrence.Frequency.DAILY,
            starts_at=self.starts_at,
        )
        defaults.update(overrides)
        if "template_task" not in defaults:
            defaults["template_task"] = self._create_task(title="Template task")
        return TaskRecurrence(**defaults)

    def _create_recurrence(self, **overrides):
        recurrence = self._build_recurrence(**overrides)
        recurrence.save()
        return recurrence

    def assertViolatesConstraint(self, instance, constraint_name):
        with self.assertRaises(IntegrityError) as ctx:
            with transaction.atomic():
                instance.save()
        # Both Postgres and SQLite name the violated constraint in the error,
        # so this pins the failure to the intended constraint rather than a
        # neighbouring one on the same model.
        self.assertIn(constraint_name, str(ctx.exception))


class TaskRecurrenceIntervalConstraintTests(RecurrenceConstraintTestCase):
    """taskrecurrence_interval_gte_1: interval must be at least 1."""

    def test_interval_of_one_is_valid(self):
        # 1 is both the default and the lower boundary the constraint allows.
        recurrence = self._create_recurrence()
        self.assertEqual(recurrence.interval, 1)

    def test_interval_at_smallint_upper_bound_is_valid(self):
        # PositiveSmallIntegerField tops out at 32767; the constraint only
        # bounds the low end.
        recurrence = self._create_recurrence(interval=32767)
        recurrence.refresh_from_db()
        self.assertEqual(recurrence.interval, 32767)

    def test_interval_of_zero_is_rejected(self):
        self.assertViolatesConstraint(
            self._build_recurrence(interval=0),
            "taskrecurrence_interval_gte_1",
        )


class TaskRecurrenceEndAfterStartConstraintTests(RecurrenceConstraintTestCase):
    """taskrecurrence_end_gte_start: ends_at is null or >= starts_at."""

    def test_null_ends_at_is_valid(self):
        recurrence = self._create_recurrence(ends_at=None)
        self.assertIsNone(recurrence.ends_at)

    def test_ends_at_equal_to_starts_at_is_valid(self):
        # >= makes the single-occurrence window (start == end) legal.
        recurrence = self._create_recurrence(ends_at=self.starts_at)
        self.assertEqual(recurrence.ends_at, recurrence.starts_at)

    def test_ends_at_after_starts_at_is_valid(self):
        recurrence = self._create_recurrence(ends_at=self.starts_at + self.day)
        self.assertGreater(recurrence.ends_at, recurrence.starts_at)

    def test_ends_at_before_starts_at_is_rejected(self):
        self.assertViolatesConstraint(
            self._build_recurrence(ends_at=self.starts_at - self.day),
            "taskrecurrence_end_gte_start",
        )


class TaskRecurrenceNextAfterStartConstraintTests(RecurrenceConstraintTestCase):
    """taskrecurrence_next_gte_start: next_occurrence_at is null or >= starts_at."""

    def test_null_next_occurrence_is_valid(self):
        recurrence = self._create_recurrence(next_occurrence_at=None)
        self.assertIsNone(recurrence.next_occurrence_at)

    def test_next_occurrence_equal_to_starts_at_is_valid(self):
        # The first occurrence may land exactly on the window start.
        recurrence = self._create_recurrence(next_occurrence_at=self.starts_at)
        self.assertEqual(recurrence.next_occurrence_at, recurrence.starts_at)

    def test_next_occurrence_after_starts_at_is_valid(self):
        recurrence = self._create_recurrence(next_occurrence_at=self.starts_at + self.day)
        self.assertGreater(recurrence.next_occurrence_at, recurrence.starts_at)

    def test_next_occurrence_before_starts_at_is_rejected(self):
        self.assertViolatesConstraint(
            self._build_recurrence(next_occurrence_at=self.starts_at - self.day),
            "taskrecurrence_next_gte_start",
        )


class TaskRecurrenceNextBeforeEndConstraintTests(RecurrenceConstraintTestCase):
    """taskrecurrence_next_lte_end: next_occurrence_at is null, ends_at is null, or next <= end."""

    def test_next_occurrence_equal_to_ends_at_is_valid(self):
        # The final occurrence may land exactly on the window end.
        recurrence = self._create_recurrence(
            ends_at=self.starts_at + self.day,
            next_occurrence_at=self.starts_at + self.day,
        )
        self.assertEqual(recurrence.next_occurrence_at, recurrence.ends_at)

    def test_next_occurrence_inside_window_is_valid(self):
        recurrence = self._create_recurrence(
            ends_at=self.starts_at + 2 * self.day,
            next_occurrence_at=self.starts_at + self.day,
        )
        self.assertLess(recurrence.next_occurrence_at, recurrence.ends_at)

    def test_next_occurrence_with_null_ends_at_is_valid(self):
        # An open-ended rule places no upper bound on the next occurrence.
        recurrence = self._create_recurrence(
            ends_at=None,
            next_occurrence_at=self.starts_at + 365 * self.day,
        )
        self.assertIsNone(recurrence.ends_at)

    def test_null_next_occurrence_with_ends_at_is_valid(self):
        # An exhausted rule (nothing left to schedule) may keep its end date.
        recurrence = self._create_recurrence(
            ends_at=self.starts_at + self.day,
            next_occurrence_at=None,
        )
        self.assertIsNone(recurrence.next_occurrence_at)

    def test_next_occurrence_after_ends_at_is_rejected(self):
        self.assertViolatesConstraint(
            self._build_recurrence(
                ends_at=self.starts_at + self.day,
                next_occurrence_at=self.starts_at + 2 * self.day,
            ),
            "taskrecurrence_next_lte_end",
        )


class TaskRecurrenceTemplateTaskTests(RecurrenceConstraintTestCase):
    """template_task is a OneToOneField: one recurrence rule per template task."""

    def test_second_rule_for_same_template_task_is_rejected(self):
        template = self._create_task(title="Shared template")
        self._create_recurrence(template_task=template)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self._build_recurrence(template_task=template).save()

    def test_distinct_template_tasks_each_get_a_rule(self):
        self._create_recurrence()
        self._create_recurrence()
        self.assertEqual(TaskRecurrence.objects.count(), 2)


class TaskRecurrenceFrequencyChoicesTests(RecurrenceConstraintTestCase):
    """Frequency choices: every declared frequency validates, anything else doesn't."""

    def test_every_frequency_choice_is_accepted(self):
        for value, _label in TaskRecurrence.Frequency.choices:
            with self.subTest(frequency=value):
                recurrence = self._build_recurrence(frequency=value)
                recurrence.full_clean()  # should not raise
                recurrence.save()
                self.assertEqual(recurrence.frequency, value)

    def test_unsupported_frequency_is_rejected(self):
        recurrence = self._build_recurrence(frequency="X")
        with self.assertRaises(ValidationError) as ctx:
            recurrence.full_clean()
        self.assertIn("frequency", ctx.exception.message_dict)


class TaskRecurrenceFieldsTogetherConstraintTests(RecurrenceConstraintTestCase):
    """
    task_recurrence_fields_together: recurrence and scheduled_for are set
    together or not at all — an occurrence must know its slot, and a slot is
    meaningless without a rule.
    """

    def test_task_with_neither_field_is_valid(self):
        task = self._create_task()
        self.assertIsNone(task.recurrence)
        self.assertIsNone(task.scheduled_for)

    def test_task_with_both_fields_is_valid(self):
        rule = self._create_recurrence()
        task = self._create_task(recurrence=rule, scheduled_for=self.starts_at)
        self.assertEqual(task.recurrence, rule)

    def test_task_with_recurrence_but_no_scheduled_for_is_rejected(self):
        rule = self._create_recurrence()
        self.assertViolatesConstraint(
            self._build_task(recurrence=rule, scheduled_for=None),
            "task_recurrence_fields_together",
        )

    def test_task_with_scheduled_for_but_no_recurrence_is_rejected(self):
        self.assertViolatesConstraint(
            self._build_task(recurrence=None, scheduled_for=self.starts_at),
            "task_recurrence_fields_together",
        )


class TaskUniqueRecurrenceSlotConstraintTests(RecurrenceConstraintTestCase):
    """
    task_unique_recurrence_slot: a rule generates at most one occurrence per
    scheduled_for slot; the condition exempts non-recurring tasks entirely.
    """

    def test_duplicate_slot_for_same_recurrence_is_rejected(self):
        rule = self._create_recurrence()
        self._create_task(recurrence=rule, scheduled_for=self.starts_at)
        self.assertViolatesConstraint(
            self._build_task(recurrence=rule, scheduled_for=self.starts_at),
            "task_unique_recurrence_slot",
        )

    def test_same_recurrence_with_distinct_slots_is_valid(self):
        rule = self._create_recurrence()
        self._create_task(recurrence=rule, scheduled_for=self.starts_at)
        self._create_task(recurrence=rule, scheduled_for=self.starts_at + self.day)
        self.assertEqual(rule.occurrences.count(), 2)

    def test_distinct_recurrences_may_share_a_slot(self):
        rule_a = self._create_recurrence()
        rule_b = self._create_recurrence()
        self._create_task(recurrence=rule_a, scheduled_for=self.starts_at)
        self._create_task(recurrence=rule_b, scheduled_for=self.starts_at)
        self.assertEqual(
            Task.objects.filter(scheduled_for=self.starts_at).count(), 2
        )

    def test_non_recurring_tasks_are_exempt_from_the_slot_constraint(self):
        # The constraint's condition (recurrence__isnull=False) means any
        # number of plain tasks can coexist despite identical null slots.
        self._create_task()
        self._create_task()
        self.assertEqual(Task.objects.filter(recurrence__isnull=True).count(), 2)
