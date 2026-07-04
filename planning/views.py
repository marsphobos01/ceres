from django.http import HttpResponse


def index(request):
    """Temporary planning landing route."""

    return HttpResponse("Planning")
