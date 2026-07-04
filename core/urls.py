from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.root_redirect, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
