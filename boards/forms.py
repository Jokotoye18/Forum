from django import forms
from . models import Topic, Post

class NewTopicForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.Textarea(attrs={"placeholder":"Enter your post"}), max_length=4000, help_text="You can only max character of 4000.")

    class Meta:
        model = Topic
        fields = ['topic', 'subject']
        widgets = {
            "topic": forms.TextInput(attrs={"placeholder":"Topic"})
        }

class NewTopicPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["post"]
        labels = {
            'post':"" 
        }
        widgets = {
            "post": forms.Textarea(attrs={"placeholder":"message"})
        }

