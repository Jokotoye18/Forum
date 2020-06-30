from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import  Profile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
