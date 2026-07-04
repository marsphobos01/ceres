from django.http import HttpResponse


def index(request):
    """Temporary content landing route."""

    return HttpResponse("Content")
