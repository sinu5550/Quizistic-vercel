from django import forms
from .models import  Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['choice','body']
        labels = {
            'choice': 'Give a Ratings',
        }
    body = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False  
        )