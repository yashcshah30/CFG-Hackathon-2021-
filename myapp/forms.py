from .models import *
from django import forms

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 1, 'cols': 70}), label='')
    class Meta:
        model = Comment
        fields = ['body']

        # def __init__(self, *args, **kwargs):
        #     super(CommentForm, self).__init__(*args, **kwargs)
        #     self.fields['email'].label = ""

        