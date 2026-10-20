from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MotherDetails, InfantDetails

INPUT_CLASS = "form-control"

class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLASS)
            if isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.setdefault("min", "0")

class MotherDetailsForm(StyledModelForm):
    class Meta:
        model = MotherDetails
        fields = [
            "mother_name", "mother_age", "education", "prenatal_visits",
            "cigarettes", "bmi", "pre_diabetes", "gest_diabetes",
            "pre_hypertension", "gest_hypertension",
        ]
        widgets = {
            "mother_age": forms.NumberInput(attrs={"min": 10, "max": 60}),
            "prenatal_visits": forms.NumberInput(attrs={"min": 0, "max": 99}),
            "cigarettes": forms.NumberInput(attrs={"min": 0, "max": 99}),
            "bmi": forms.NumberInput(attrs={"min": 10, "max": 80, "step": "0.1"}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("mother_age") is not None and not 10 <= cleaned["mother_age"] <= 60:
            self.add_error("mother_age", "Enter an age between 10 and 60.")
        if cleaned.get("bmi") is not None and not 10 <= cleaned["bmi"] <= 80:
            self.add_error("bmi", "Enter a BMI between 10 and 80, or leave it blank.")
        return cleaned

class InfantDetailsForm(StyledModelForm):
    class Meta:
        model = InfantDetails
        fields = ["mother", "apgar5", "plurality", "infant_sex", "gestational_age", "birth_weight"]
        widgets = {
            "apgar5": forms.NumberInput(attrs={"min": 0, "max": 10}),
            "plurality": forms.NumberInput(attrs={"min": 1, "max": 8}),
            "gestational_age": forms.NumberInput(attrs={"min": 1, "max": 45}),
            "birth_weight": forms.NumberInput(attrs={"min": 100, "max": 7000}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("apgar5") is not None and not 0 <= cleaned["apgar5"] <= 10:
            self.add_error("apgar5", "Apgar score must be between 0 and 10.")
        return cleaned


class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True, label="First name", widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Enter your first name"}))
    last_name = forms.CharField(max_length=150, required=True, label="Last name", widget=forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Enter your last name"}))
    email = forms.EmailField(required=True, label="Email address", widget=forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "doctor@example.com"}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", INPUT_CLASS)
        self.fields["username"].widget.attrs.setdefault("placeholder", "Choose a username")
        self.fields["password1"].widget.attrs.setdefault("placeholder", "Create a strong password")
        self.fields["password2"].widget.attrs.setdefault("placeholder", "Enter the password again")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists.")
        return email
