from django import forms

from .models import Document, Location, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["description", "from_location", "to_location", "driver"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "from_location": forms.TextInput(attrs={"class": "form-control"}),
            "to_location": forms.TextInput(attrs={"class": "form-control"}),
            "driver": forms.Select(attrs={"class": "form-select"}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["file"]
        widgets = {"file": forms.ClearableFileInput(attrs={"class": "form-control", "required": True})}

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if not file:
            raise forms.ValidationError("Необходимо загрузить файл.")
        return file


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ("order", "latitude", "longitude", "timestamp")
        widgets = {
            "order": forms.Select(attrs={"class": "form-select"}),
            "driver": forms.Select(attrs={"class": "form-select"}),
            "latitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.000001",
                    "placeholder": "Широта (-90 .. 90)",
                }
            ),
            "longitude": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.000001",
                    "placeholder": "Долгота (-180 .. 180)",
                }
            ),
            "timestamp": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Отключаем локализацию для полей широты и долготы
        self.fields["latitude"].localize = False
        self.fields["longitude"].localize = False
