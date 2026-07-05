from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import CreateUserForm


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('accounts:login')
    else:
        form = CreateUserForm()

    return render(request, 'registration/register.html', {'form': form})