from django import forms

from .models import Comment

class EmailPostForm(forms.Form):
    """
    form for sending post to somebody
    name:: name of user
    email_from:: from who
    email_to:: to who
    comment:: some comment
    """
    name = forms.CharField(max_length=28, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_from = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email_to = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):
    """
    form for adding comment to posts
    """
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


