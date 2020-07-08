from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages
from .forms import UserProfileForm, UserUpdateForm


class UserProfileView(LoginRequiredMixin, View):
    login_url = 'account_login'
    def get(self, request, *args, **kwargs):
        form_user = UserUpdateForm(instance=request.user)
        form_profile = UserProfileForm()
        context = {'form_user':form_user, 'form_profile':form_profile}
        return render(request, 'profile.html', context)

    def post(self, request, *args, **kwargs):
        form_user = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        form_profile = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form_profile.is_valid() and form_user.is_valid():
            form_user.save()
            form_profile.save()
            messages.info(request, 'profile updated successfully')
            return redirect(reverse('profiles:profile'))


