from django.http import HttpResponse


def index(request):
    """Temporary global search landing route."""

    return HttpResponse("Search")
