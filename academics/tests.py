from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.test import TestCase

from .models import Assignment, AssignmentParticipant, Module, ModuleMembership


class AssignmentParticipantTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.module_owner = user_model.objects.create_user(
            username="module-owner",
            password="test-password",
        )
        self.owner_member = user_model.objects.create_user(
            username="owner-member",
            password="test-password",
        )
        self.member = user_model.objects.create_user(
            username="module-member",
            password="test-password",
        )
        self.viewer = user_model.objects.create_user(
            username="module-viewer",
            password="test-password",
        )
        self.outsider = user_model.objects.create_user(
            username="outsider",
            password="test-password",
        )

        self.module = Module.objects.create(
            owner=self.module_owner,
            title="Network Security",
        )
        ModuleMembership.objects.create(
            module=self.module,
            user=self.owner_member,
            role=ModuleMembership.Role.OWNER,
        )
        ModuleMembership.objects.create(
            module=self.module,
            user=self.member,
            role=ModuleMembership.Role.MEMBER,
        )
        ModuleMembership.objects.create(
            module=self.module,
            user=self.viewer,
            role=ModuleMembership.Role.VIEWER,
        )

        self.group_assignment = Assignment.objects.create(
            module=self.module,
            title="Group report",
            is_group=True,
        )
        self.individual_assignment = Assignment.objects.create(
            module=self.module,
            title="Individual report",
            is_group=False,
        )

    def test_module_member_can_be_added_to_group_assignment(self):
        participant = AssignmentParticipant.objects.create(
            assignment=self.group_assignment,
            user=self.member,
        )

        self.assertEqual(participant.assignment, self.group_assignment)
        self.assertIn(self.member, self.group_assignment.participants.all())
        self.assertIn(
            self.group_assignment,
            self.member.participating_assignments.all(),
        )

    def test_module_owner_can_be_added_without_membership_row(self):
        participant = AssignmentParticipant.objects.create(
            assignment=self.group_assignment,
            user=self.module_owner,
        )

        self.assertEqual(participant.user, self.module_owner)

    def test_duplicate_participant_is_rejected(self):
        AssignmentParticipant.objects.create(
            assignment=self.group_assignment,
            user=self.member,
        )

        with self.assertRaises(ValidationError):
            AssignmentParticipant.objects.create(
                assignment=self.group_assignment,
                user=self.member,
            )

    def test_individual_assignment_rejects_participants(self):
        with self.assertRaises(ValidationError):
            AssignmentParticipant.objects.create(
                assignment=self.individual_assignment,
                user=self.member,
            )

    def test_user_without_module_access_is_rejected(self):
        with self.assertRaises(ValidationError):
            AssignmentParticipant.objects.create(
                assignment=self.group_assignment,
                user=self.outsider,
            )

    def test_many_to_many_add_uses_participant_validation(self):
        # ManyRelatedManager.add() uses an atomic block without a savepoint.
        # Isolate the expected validation error in our own savepoint so the
        # surrounding TestCase transaction remains usable for the valid add.
        with self.assertRaises(ValidationError):
            with transaction.atomic():
                self.group_assignment.participants.add(self.outsider)

        self.group_assignment.participants.add(self.member)
        self.assertTrue(
            AssignmentParticipant.objects.filter(
                assignment=self.group_assignment,
                user=self.member,
            ).exists()
        )

    def test_group_assignment_cannot_become_individual_with_participants(self):
        AssignmentParticipant.objects.create(
            assignment=self.group_assignment,
            user=self.member,
        )
        self.group_assignment.is_group = False

        with self.assertRaises(ValidationError):
            self.group_assignment.save()

    def test_module_owner_and_owner_member_can_manage_participants(self):
        self.assertTrue(
            self.group_assignment.can_manage_participants(self.module_owner)
        )
        self.assertTrue(
            self.group_assignment.can_manage_participants(self.owner_member)
        )

    def test_regular_members_and_viewers_cannot_manage_participants(self):
        self.assertFalse(self.group_assignment.can_manage_participants(self.member))
        self.assertFalse(self.group_assignment.can_manage_participants(self.viewer))
        self.assertFalse(self.group_assignment.can_manage_participants(self.outsider))

    def test_participant_membership_does_not_grant_edit_permission(self):
        AssignmentParticipant.objects.create(
            assignment=self.group_assignment,
            user=self.member,
        )

        self.assertFalse(self.group_assignment.can_manage_participants(self.member))

    def test_add_participant_requires_an_authorised_actor(self):
        with self.assertRaises(PermissionDenied):
            self.group_assignment.add_participant(
                actor=self.member,
                user=self.viewer,
            )

        participant = self.group_assignment.add_participant(
            actor=self.module_owner,
            user=self.viewer,
        )
        self.assertEqual(participant.user, self.viewer)

    def test_remove_participant_requires_an_authorised_actor(self):
        AssignmentParticipant.objects.create(
            assignment=self.group_assignment,
            user=self.member,
        )

        with self.assertRaises(PermissionDenied):
            self.group_assignment.remove_participant(
                actor=self.member,
                user=self.member,
            )

        self.group_assignment.remove_participant(
            actor=self.owner_member,
            user=self.member,
        )
        self.assertFalse(
            AssignmentParticipant.objects.filter(
                assignment=self.group_assignment,
                user=self.member,
            ).exists()
        )

    def test_deleting_assignment_removes_participant_rows(self):
        AssignmentParticipant.objects.create(
            assignment=self.group_assignment,
            user=self.member,
        )
        assignment_id = self.group_assignment.pk

        self.group_assignment.delete()

        self.assertFalse(
            AssignmentParticipant.objects.filter(
                assignment_id=assignment_id,
            ).exists()
        )
