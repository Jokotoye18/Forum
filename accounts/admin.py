from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .forms import  CustomUserChangeForm, CustomUserCreationForm
from .models import Profile

# class CustomUserAdmin(UserAdmin):
#     form = CustomUserChangeForm
#     add_form = CustomUserCreationForm
#     model = CustomUser

# admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Profile)