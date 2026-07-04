from django.http import HttpResponse


def index(request):
    """Temporary files landing route."""

    return HttpResponse("Files")
