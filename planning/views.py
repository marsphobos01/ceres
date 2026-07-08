from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
@login_required
def index(request):
    


    return  render(request, "planning/calendar.html")




