from django.contrib.auth.forms import UserCreationForm
from django import forms

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True) # Email should be required when creating a user - not just a reccomendation
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'password1', 'password2')
