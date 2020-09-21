from django import forms
from posts.models import *

class PostsForm(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ('post_text','post_pic')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)