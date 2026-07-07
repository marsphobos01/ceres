import re
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase, TestCase
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


class FrontendVisualRulesTests(SimpleTestCase):
    """Guard permanent visual rules shared by every Ceres feature."""

    UI_FILE_SUFFIXES = {".css", ".html"}
    EXCLUDED_DIRECTORIES = {".git", ".venv", "venv", "node_modules", "staticfiles"}

    FORBIDDEN_SIDE_HIGHLIGHTS = {
        "thick one-sided border": re.compile(
            r"border-(?:left|right)(?:-width)?\s*:\s*"
            r"(?:[2-9]|\d{2,})px\b|"
            r"border-(?:left|right)(?:-width)?\s*:\s*"
            r"(?:0?\.[2-9]|[1-9]\d*\.?\d*)rem\b",
            re.IGNORECASE,
        ),
        "side-specific state colour": re.compile(
            r"border-(?:left|right)-color\s*:",
            re.IGNORECASE,
        ),
        "inset side strip": re.compile(
            r"box-shadow\s*:\s*inset\s+"
            r"-?(?:\d*\.)?\d+(?:px|rem|em)\s+0(?:px|rem|em)?\b",
            re.IGNORECASE,
        ),
    }

    def test_ui_files_do_not_use_side_highlight_strips(self):
        repository_root = Path(settings.BASE_DIR)
        failures = []

        for path in repository_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in self.UI_FILE_SUFFIXES:
                continue
            if any(part in self.EXCLUDED_DIRECTORIES for part in path.parts):
                continue

            content = path.read_text(encoding="utf-8")
            relative_path = path.relative_to(repository_root)

            for rule_name, pattern in self.FORBIDDEN_SIDE_HIGHLIGHTS.items():
                for match in pattern.finditer(content):
                    line_number = content.count("\n", 0, match.start()) + 1
                    failures.append(
                        f"{relative_path}:{line_number}: {rule_name}: {match.group(0)!r}"
                    )

        self.assertFalse(
            failures,
            "Side highlight strips are banned from Ceres UI components:\n"
            + "\n".join(failures),
        )


class DashboardTemplateTests(TestCase):
    def test_dashboard_renders_using_base_template_when_authenticated(self):
        user = get_user_model().objects.create_user(
            username="dashboard-template-user",
            password="test-password-123",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("core:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "base.html")


class StaticAssetTests(SimpleTestCase):
    def test_base_stylesheet_is_served(self):
        # STATIC_URL is normalised by Django to already include a leading
        # slash, even though settings.py defines it as 'static/'.
        response = self.client.get(f"{settings.STATIC_URL}css/base.css")

        self.assertEqual(response.status_code, 200)
