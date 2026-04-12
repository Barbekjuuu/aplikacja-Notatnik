from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        labels = {
            'title': 'Tytuł notatki',
            'content': 'Treść notatki',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }