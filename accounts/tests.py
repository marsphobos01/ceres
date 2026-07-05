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


class ProtectedViewRedirectTests(TestCase):
    def test_anonymous_user_is_redirected_to_login_with_next(self):
        dashboard_url = reverse("core:dashboard")
        response = self.client.get(dashboard_url)

        expected_redirect = f"{reverse('accounts:login')}?next={dashboard_url}"
        self.assertRedirects(response, expected_redirect)
