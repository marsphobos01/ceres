from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Temporary content landing route."""

    return HttpResponse("Content")
