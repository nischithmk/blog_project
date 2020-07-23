from django import forms
from .models import Post,Comment
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author','title','text','photo')

        widgets = {
         'title':forms.TextInput(attrs={'class':'textinputclass'}),
          'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author','text')


        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ('username','email','password')
        help_texts = {
            'username': None,
        }