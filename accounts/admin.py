from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import  CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser

admin.site.register(CustomUser, CustomUserAdmin)