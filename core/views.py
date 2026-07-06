from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render


def root_redirect(request):
    """Send users to the appropriate entry point."""

    if request.user.is_authenticated:
        return redirect("core:dashboard")

    return redirect("accounts:login")

@login_required
def dashboard(request):
    """Temporary application landing shell."""

    return render(request, "core/dashboard.html")
