from django import forms
from .models import CalendarEvent
from core.form_fields import HexColourField
class CalendarForm(forms.ModelForm):
    colour = HexColourField(required=False)
    class Meta:
        model = CalendarEvent
        fields = [
            "title",
            "description",
            "start",
            "3nd",
            "all day",
            "location",
            "recurrence",
            "colour"
        ]
