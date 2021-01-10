from django import forms
from blog.models import Comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments

        fields= [
            'name',
            'content',
        ]