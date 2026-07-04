from django.http import HttpResponse


def index(request):
    """Temporary collaboration landing route."""

    return HttpResponse("Collaboration")
