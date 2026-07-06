from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

VALID_PASSWORD = "a-very-uncommon-pass123"


class RegistrationTests(TestCase):
    def test_user_can_register(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "newstudent",
            "email": "newstudent@example.com",
            "password1": VALID_PASSWORD,
            "password2": VALID_PASSWORD,
        })

        self.assertRedirects(response, reverse("accounts:login"))
        self.assertTrue(User.objects.filter(username="newstudent").exists())

    def test_registration_shows_success_message(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "newstudent2",
            "email": "newstudent2@example.com",
            "password1": VALID_PASSWORD,
            "password2": VALID_PASSWORD,
        }, follow=True)

        shown_messages = [str(message) for message in response.context["messages"]]
        self.assertTrue(any("created" in message for message in shown_messages))

    def test_registration_requires_email(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "noemail",
                "email": "",
                "password1": VALID_PASSWORD,
                "password2": VALID_PASSWORD,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "email", "This field is required.")
        self.assertFalse(User.objects.filter(username="noemail").exists())


    def test_registration_rejects_common_password(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "weakpassword",
                "email": "weak@example.com",
                "password1": "password",
                "password2": "password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="weakpassword").exists())



class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="existing", password=VALID_PASSWORD)

    def test_user_can_log_in_and_is_redirected_to_dashboard(self):
        response = self.client.post(reverse("accounts:login"), {
            "username": "existing",
            "password": VALID_PASSWORD,
        })

        self.assertRedirects(response, reverse("core:dashboard"))


class LogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="existing", password=VALID_PASSWORD)
        self.client.login(username="existing", password=VALID_PASSWORD)

    def test_logout_clears_session_and_redirects_to_login(self):
        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(response, reverse("accounts:login"))
        self.assertNotIn("_auth_user_id", self.client.session)


class ProtectedViewRedirectTests(TestCase): # Check ALL routes, not just core.
    protected_routes = [
        "core:dashboard",
        "academics:index",
        "planning:index",
        "content:index",
        "collaboration:index",
        "files:index",
        "notifications:index",
        "search:index",
    ]

    def test_anonymous_users_are_redirected_to_login(self):
        for route_name in self.protected_routes:
            with self.subTest(route=route_name):
                url = reverse(route_name)
                response = self.client.get(url)

                expected_redirect = (
                    f"{reverse('accounts:login')}?next={url}"
                )

                self.assertRedirects(response, expected_redirect)
