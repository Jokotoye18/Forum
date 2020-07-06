from django import forms
from . models import Topic, Post
from ckeditor.widgets import CKEditorWidget

class NewTopicForm(forms.ModelForm):
    subject = forms.CharField(widget=CKEditorWidget(), max_length=400, help_text='max char of 400') #SummernoteTextFormField()
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
        widgets = {
            # 'post': CKEditorWidget(attrs={"placeholder":"message"})
        }

