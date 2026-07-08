from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.test import TestCase
from django.urls import reverse
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

class ModuleViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()

        self.user = user_model.objects.create_user(
            username="morgan",
            password="test-password",
        )

        self.other_user = user_model.objects.create_user(
            username="tom",
            password="test-password",
        )

        self.module = Module.objects.create(
            owner=self.user,
            title="Network Security",
            code="NX101",
            description="Introductory network security module.",
            colour="713D5A",
            academic_year="2026/2027",
            semester="autumn",
        )

    def test_module_list_requires_login(self):
        response = self.client.get(reverse("academics:module_list"))

        self.assertEqual(response.status_code, 302)

    def test_owner_can_see_module_in_list(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.get(reverse("academics:module_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Network Security")

    def test_other_user_cannot_see_module_in_list(self):
        self.client.login(username="tom", password="test-password")

        response = self.client.get(reverse("academics:module_list"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Network Security")

    def test_owner_can_view_module_detail(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.get(
            reverse("academics:module_detail", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Network Security")
        self.assertContains(response, "NX101")

    def test_other_user_gets_404_for_module_detail(self):
        self.client.login(username="tom", password="test-password")

        response = self.client.get(
            reverse("academics:module_detail", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_user_can_create_module(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.post(
            reverse("academics:module_create"),
            {
                "title": "Databases",
                "code": "DB101",
                "description": "Database fundamentals.",
                "colour": "#123ABC",
                "academic_year": "2026/2027",
                "semester": "spring",
            },
        )

        module = Module.objects.get(title="Databases")

        self.assertEqual(module.owner, self.user)
        self.assertEqual(module.colour, "123ABC")
        self.assertRedirects(
            response,
            reverse("academics:module_detail", kwargs={"pk": module.pk}),
        )

    def test_owner_can_edit_module(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.post(
            reverse("academics:module_edit", kwargs={"pk": self.module.pk}),
            {
                "title": "Advanced Network Security",
                "code": "NX201",
                "description": "Updated module description.",
                "colour": "#ABC123",
                "academic_year": "2026/2027",
                "semester": "spring",
            },
        )

        self.module.refresh_from_db()

        self.assertEqual(self.module.title, "Advanced Network Security")
        self.assertEqual(self.module.code, "NX201")
        self.assertEqual(self.module.colour, "ABC123")
        self.assertRedirects(
            response,
            reverse("academics:module_detail", kwargs={"pk": self.module.pk}),
        )

    def test_other_user_cannot_edit_module(self):
        self.client.login(username="tom", password="test-password")

        response = self.client.post(
            reverse("academics:module_edit", kwargs={"pk": self.module.pk}),
            {
                "title": "Hacked title",
                "code": "BAD101",
                "description": "Should not save.",
                "colour": "#000000",
                "academic_year": "2026/2027",
                "semester": "spring",
            },
        )

        self.module.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.module.title, "Network Security")
        self.assertEqual(self.module.code, "NX101")


    def test_owner_can_open_delete_confirmation(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.get(
            reverse("academics:module_delete", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete module")
        self.assertContains(response, "Network Security")

    def test_owner_can_delete_module(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.post(
            reverse("academics:module_delete", kwargs={"pk": self.module.pk})
        )

        self.assertFalse(Module.objects.filter(pk=self.module.pk).exists())
        self.assertRedirects(response, reverse("academics:module_list"))

    def test_other_user_cannot_delete_module(self):
        self.client.login(username="tom", password="test-password")

        response = self.client.post(
            reverse("academics:module_delete", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Module.objects.filter(pk=self.module.pk).exists())

    def test_get_delete_page_does_not_delete_module(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.get(
            reverse("academics:module_delete", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Module.objects.filter(pk=self.module.pk).exists())

    def test_module_create_requires_login(self):
        response = self.client.get(reverse("academics:module_create"))

        self.assertEqual(response.status_code, 302)

    def test_module_detail_requires_login(self):
        response = self.client.get(
            reverse("academics:module_detail", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 302)

    def test_module_edit_requires_login(self):
        response = self.client.get(
            reverse("academics:module_edit", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 302)

    def test_module_delete_requires_login(self):
        response = self.client.get(
            reverse("academics:module_delete", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 302)

    def test_module_create_requires_title(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.post(
            reverse("academics:module_create"),
            {
                "title": "",
                "code": "BAD101",
                "description": "Missing title.",
                "colour": "#123ABC",
                "academic_year": "2026/2027",
                "semester": "spring",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Module.objects.filter(code="BAD101").exists())

    def test_module_create_rejects_invalid_colour(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.post(
            reverse("academics:module_create"),
            {
                "title": "Invalid Colour Module",
                "code": "BAD102",
                "description": "Invalid colour test.",
                "colour": "#ZZZZZZ",
                "academic_year": "2026/2027",
                "semester": "spring",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Module.objects.filter(title="Invalid Colour Module").exists())

    def test_posted_owner_is_ignored_when_creating_module(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.post(
            reverse("academics:module_create"),
            {
                "title": "Ownership Test",
                "code": "OWN101",
                "description": "Trying to spoof owner.",
                "colour": "#123ABC",
                "academic_year": "2026/2027",
                "semester": "spring",
                "owner": self.other_user.pk,
            },
        )

        module = Module.objects.get(title="Ownership Test")

        self.assertEqual(module.owner, self.user)
        self.assertNotEqual(module.owner, self.other_user)
        self.assertRedirects(
            response,
            reverse("academics:module_detail", kwargs={"pk": module.pk}),
        )

    def test_module_does_not_duplicate_in_list_when_user_is_owner_and_member(self):
        ModuleMembership.objects.create(
            module=self.module,
            user=self.user,
            role=ModuleMembership.Role.OWNER,
        )

        self.client.login(username="morgan", password="test-password")

        response = self.client.get(reverse("academics:module_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Network Security", count=1)

    def test_module_viewer_can_see_shared_module_in_list(self):
        ModuleMembership.objects.create(
            module=self.module,
            user=self.other_user,
            role=ModuleMembership.Role.VIEWER,
        )

        self.client.login(username="tom", password="test-password")

        response = self.client.get(reverse("academics:module_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Network Security")

    def test_module_viewer_can_view_shared_module_detail(self):
        ModuleMembership.objects.create(
            module=self.module,
            user=self.other_user,
            role=ModuleMembership.Role.VIEWER,
        )

        self.client.login(username="tom", password="test-password")

        response = self.client.get(
            reverse("academics:module_detail", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Network Security")
        self.assertContains(response, "NX101")

    def test_module_viewer_cannot_edit_shared_module(self):
        ModuleMembership.objects.create(
            module=self.module,
            user=self.other_user,
            role=ModuleMembership.Role.VIEWER,
        )

        self.client.login(username="tom", password="test-password")

        response = self.client.post(
            reverse("academics:module_edit", kwargs={"pk": self.module.pk}),
            {
                "title": "Changed by viewer",
                "code": "BAD201",
                "description": "Should not save.",
                "colour": "#000000",
                "academic_year": "2026/2027",
                "semester": "spring",
            },
        )

        self.module.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.module.title, "Network Security")
        self.assertEqual(self.module.code, "NX101")

    def test_module_viewer_cannot_delete_shared_module(self):
        ModuleMembership.objects.create(
            module=self.module,
            user=self.other_user,
            role=ModuleMembership.Role.VIEWER,
        )

        self.client.login(username="tom", password="test-password")

        response = self.client.post(
            reverse("academics:module_delete", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Module.objects.filter(pk=self.module.pk).exists())

    def test_invalid_edit_does_not_overwrite_existing_module(self):
        self.client.login(username="morgan", password="test-password")

        response = self.client.post(
            reverse("academics:module_edit", kwargs={"pk": self.module.pk}),
            {
                "title": "Broken Edit",
                "code": "BROKEN",
                "description": "This should not save.",
                "colour": "#ZZZZZZ",
                "academic_year": "2026/2027",
                "semester": "spring",
            },
        )

        self.module.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.module.title, "Network Security")
        self.assertEqual(self.module.code, "NX101")
        self.assertEqual(self.module.colour, "713D5A")


    def test_module_member_can_see_shared_module_in_list(self):
        ModuleMembership.objects.create(
            module=self.module,
            user=self.other_user,
            role=ModuleMembership.Role.MEMBER,
        )

        self.client.login(username="tom", password="test-password")

        response = self.client.get(reverse("academics:module_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Network Security")

    def test_module_member_can_view_shared_module_detail(self):
        ModuleMembership.objects.create(
            module=self.module,
            user=self.other_user,
            role=ModuleMembership.Role.MEMBER,
        )

        self.client.login(username="tom", password="test-password")

        response = self.client.get(
            reverse("academics:module_detail", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Network Security")
        self.assertContains(response, "NX101")

    def test_module_member_cannot_edit_shared_module(self):
        ModuleMembership.objects.create(
            module=self.module,
            user=self.other_user,
            role=ModuleMembership.Role.MEMBER,
        )

        self.client.login(username="tom", password="test-password")

        response = self.client.post(
            reverse("academics:module_edit", kwargs={"pk": self.module.pk}),
            {
                "title": "Changed by member",
                "code": "BAD101",
                "description": "Should not save.",
                "colour": "#000000",
                "academic_year": "2026/2027",
                "semester": "spring",
            },
        )

        self.module.refresh_from_db()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.module.title, "Network Security")
        self.assertEqual(self.module.code, "NX101")

    def test_module_member_cannot_delete_shared_module(self):
        ModuleMembership.objects.create(
            module=self.module,
            user=self.other_user,
            role=ModuleMembership.Role.MEMBER,
        )

        self.client.login(username="tom", password="test-password")

        response = self.client.post(
            reverse("academics:module_delete", kwargs={"pk": self.module.pk})
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Module.objects.filter(pk=self.module.pk).exists())
