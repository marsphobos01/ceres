from django.urls import path

from . import views

app_name = "academics"

urlpatterns = [
    path("", views.index, name="index"),

    path("modules/", views.module_list, name="module_list"),
    path("modules/create/", views.module_create, name="module_create"),
    path("modules/<int:pk>/", views.module_detail, name="module_detail"),
    path("modules/<int:pk>/edit/", views.module_edit, name="module_edit"),
    path("modules/<int:pk>/delete/", views.module_delete, name="module_delete")
]
