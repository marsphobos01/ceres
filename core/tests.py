from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class URLReverseTests(TestCase):
    def test_named_routes_reverse_to_expected_paths(self):
        routes = {
            "core:index": "/",
            "core:dashboard": "/dashboard/",
            "accounts:login": "/accounts/login/",
            "academics:index": "/academics/",
            "collaboration:index": "/collaboration/",
            "content:index": "/content/",
            "files:index": "/files/",
            "notifications:index": "/notifications/",
            "planning:index": "/planning/",
            "search:index": "/search/",
        }

        for route_name, expected_path in routes.items():
            with self.subTest(route_name=route_name):
                self.assertEqual(reverse(route_name), expected_path)


class RootRedirectTests(TestCase):
    def test_unauthenticated_user_is_redirected_to_login(self):
        response = self.client.get(reverse("core:index"))

        self.assertRedirects(
            response,
            reverse("accounts:login"),
            fetch_redirect_response=False,
        )

    def test_authenticated_user_is_redirected_to_dashboard(self):
        user = get_user_model().objects.create_user(
            username="routing-test-user",
            password="test-password-123",
        )

        self.client.force_login(user)

        response = self.client.get(reverse("core:index"))

        self.assertRedirects(
            response,
            reverse("core:dashboard"),
            fetch_redirect_response=False,
        )


class RouteResponseTests(TestCase):
    def test_temporary_app_index_routes_are_accessible(self):
        route_names = [
            "core:dashboard",
            "academics:index",
            "collaboration:index",
            "content:index",
            "files:index",
            "notifications:index",
            "planning:index",
            "search:index",
        ]

        for route_name in route_names:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
