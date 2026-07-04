from django.http import HttpResponse


def index(request):
    """Temporary notifications landing route."""

    return HttpResponse("Notifications")
