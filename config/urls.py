from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("core.urls")),

    path("accounts/", include("accounts.urls")),
    path("academics/", include("academics.urls")),
    path("collaboration/", include("collaboration.urls")),
    path("content/", include("content.urls")),
    path("files/", include("files.urls")),
    path("notifications/", include("notifications.urls")),
    path("planning/", include("planning.urls")),
    path("search/", include("search.urls")),
]

if settings.DEBUG:
    # Serve STATICFILES_DIRS through Django itself in development (and for
    # the test client, which never goes through runserver's own static
    # handling). Never relied on in production - DEBUG is False there and
    # static files are served by the web server / CDN instead.
    urlpatterns += staticfiles_urlpatterns()
