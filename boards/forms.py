from django import forms
from . models import Topic, Post
from martor.fields import MartorFormField

class NewTopicForm(forms.ModelForm):
    subject = MartorFormField()
    class Meta:
        model = Topic
        fields = ['topic', 'subject',]
        widgets = {
            "topic": forms.TextInput(attrs={"placeholder":"Topic"}),
        }

class NewTopicPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["post",]

