from django import forms
from .models import Note


class AppNoteUpdateForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(AppNoteUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget = forms.widgets.TextInput(attrs={
            'id': 'note-form-title',
            'class': 'border-0 bg-light',
            'contenteditable': 'true'
        })
        self.fields['content'].widget = forms.widgets.Textarea(attrs={
            'id': 'note-form-content',
            'class': 'form-control',
            'rows': '25',
        })
        self.fields['title'].required = False
        self.fields['title'].label = ''
        self.fields['content'].required = False
        self.fields['content'].label = ''



