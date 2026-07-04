from django.http import HttpResponse


def index(request):
    """Temporary academics landing route."""

    return HttpResponse("Academics")
