from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Note   # ← ważne!

# ====================== ORYGINALNY FORMULARZ NOTATKI ======================
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category']


# ====================== LEKCJA 24 - ZADANIE 6 ======================
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Adres email",
        help_text="Podaj swój adres email."
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user