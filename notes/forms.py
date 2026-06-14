from django import forms
from .models import Note
from django.utils.translation import gettext_lazy as _

class NoteForm(forms.ModelForm):
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Add tags separated by commas: python, integrals, totalitarism...')}),
        label=_('Tags')
    )

    class Meta:
        model = Note
        fields = ['title', 'course', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Note title...')}),
            'content': forms.Textarea(attrs={'placeholder': _('Write your note here...'), 'rows': 15}),
        }
        labels = {
            'title': _('Title'),
            'course': _('Course'),
            'content': _('Content'),
        }