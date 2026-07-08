from django import forms
from .models import Module
from core.form_fields import HexColourField

class ModuleForm(forms.ModelForm):
    colour = HexColourField(required=False)
    class Meta:
        model = Module
        fields = [
            "title",
            "code",
            "description",
            "colour",
            "academic_year",
            "semester",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class":"input"}),
            "code": forms.TextInput(attrs={"class":"input"}),
            "description": forms.Textarea(attrs={"class":"textarea","rows": 5}),
            "academic_year": forms.TextInput(attrs={"class":"input"}),
            "semester": forms.Select(attrs={"class":"select"}),
        }
