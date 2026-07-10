from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Module
from django.contrib import messages
from .forms import ModuleForm

@login_required
def index(request):
    """Temporary academics landing route."""

    return HttpResponse("Academics")

@login_required
def module_list(request):
    # List all modules that the user owns or is a member of
    modules = (
        Module.objects.filter(
            Q(owner=request.user) | Q(memberships__user=request.user)
        )
        .distinct()
        .order_by("title")
    )

    return render(
        request,
        "academics/module_list.html",
        {
            "modules": modules,
        },
    )

@login_required
def module_create(request):
    if request.method == "POST":
        # The form is the specialised form we made in forms.py
        form = ModuleForm(request.POST)

        # Checks if the form is valid ( matches the model )
        if form.is_valid():
            module = form.save(commit=False)
            # Sets the owner to whoever made the request
            module.owner = request.user
            # Save it to the DB
            module.save()

            # Success!
            messages.success(request, "Module created successfully.")
            return redirect("academics:module_detail", pk=module.pk)
    # If its a GET request, give them the form
    else:
        form = ModuleForm()

    # Return the form to the user, with a mode of create so the template knows what to do
    return render(
        request,
        "academics/module_form.html",
        {
            "form": form,
            "mode": "create",
        },
    )

@login_required
def module_detail(request,pk):
    # Find the module with the given pk, but only if the user is the owner or a member of it
    module = get_object_or_404(
        Module.objects.filter(
            Q(owner=request.user) | Q(memberships__user=request.user)
        ).distinct(),
        pk=pk
    )
    lectures = module.lectures.order_by("date","pk")

    can_edit = module.owner == request.user
    can_delete = module.owner == request.user

    # Render the module detail template with the module
    return render(
        request,
        "academics/module_detail.html",
        {
            "module": module,
            "can_edit": can_edit,
            "can_delete": can_delete,
            "lectures":lectures,
        },
    )


@login_required
def module_edit(request,pk):
    # Find the module with the given pk, but only if the user is the owner of it
    module = get_object_or_404(
        Module.objects.filter(owner=request.user),
        pk=pk,
    )

    # If the request is a POST, we are submitting the form, so we need to validate and save it
    if request.method == "POST":
        form = ModuleForm(request.POST, instance=module)

        # If the form is valid, save it and redirect to the module detail page
        if form.is_valid():
            form.save()
            messages.success(request, "Module updated successfully.")
            return redirect("academics:module_detail", pk=module.pk)

    # If the request is a GET, we are just displaying the form, so we need to populate it with the module data
    else:
        form = ModuleForm(instance=module)

    return render(
        request,
        "academics/module_form.html",
        {
            "form": form,
            "mode": "edit",
            "module": module,
        },
    )

@login_required
def module_delete(request,pk):
    # Find the module with the given pk, but only if the user is the owner of it
    module = get_object_or_404(
        Module.objects.filter(owner=request.user),
        pk=pk,
    )
    # If the request is a POST, we are confirming the deletion, so we need to delete the module and redirect to the module list page
    if request.method == "POST":
        module.delete()
        messages.success(request, "Module deleted successfully.")
        return redirect("academics:module_list")

    return render(
        request,
        "academics/module_confirm_delete.html",
        {
            "module": module,
        },
    )
