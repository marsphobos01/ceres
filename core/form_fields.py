import re

from django import forms


HEX_COLOUR_RE = re.compile(r"^[0-9a-fA-F]{6}$")


class HexColourField(forms.CharField):
    widget = forms.TextInput(attrs={"type": "color", "class": "input"})

    def prepare_value(self, value):
        if not value:
            return value

        value = str(value).strip()

        if value.startswith("#"):
            return value

        return f"#{value}"

    def to_python(self, value):
        value = super().to_python(value)

        if not value:
            return ""

        value = value.strip()

        if value.startswith("#"):
            value = value[1:]

        return value.upper()

    def validate(self, value):
        super().validate(value)

        if not value:
            return

        if not HEX_COLOUR_RE.match(value):
            raise forms.ValidationError("Enter a valid 6-character hex colour.")
