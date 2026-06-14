from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Add tags separated by commas: python, integrals, totalitarism...'}),
        label='Tags'
    )

    class Meta:
        model = Note
        fields = ['title', 'course', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Note title...'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your note here...', 'rows': 15}),
        }