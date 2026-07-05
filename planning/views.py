from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def index(request):
    """Temporary planning landing route."""

    return HttpResponse("Planning")
