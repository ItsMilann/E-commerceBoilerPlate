from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegisterForm, UserUpdate, ProfileUpdate
from .models import Profile
from django.contrib.auth.forms import UserCreationForm as SignUpForm
from django.contrib.auth import logout, login, authenticate
from products.models import Order

class Register(View):
    def get(self, *args, **kwargs):
        form = RegisterForm
        context = {'form':form}
        return render(self.request, 'registration/sign-up.html', context)
    
    def post(self, *args, **kwargs):
        form = RegisterForm(self.request.POST)
        context = {'form':form}
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(self.request, username=username, password=password)
            login(self.request, user)
            profile = Profile(
                user=self.request.user
            )
            profile.save()
            messages.success(self.request, 'Account created succesfully.')
            return redirect('home')
        else:
            messages.warning(self.request, 'Please correct the errors below and try again.')
        return render(self.request, 'registration/sign-up.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out!")
    return redirect('login')


class ProfileView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user, ordered = True)
        context = {'order': order}
        return render(self.request, 'registration/profile.html', context)

class ProfileUpdateView(View):
    def get(self, *args, **kwargs):
        user_form = UserUpdate(instance=self.request.user)
        profile_form = ProfileUpdate(instance=self.request.user.profile)
        context = {'u_form': user_form, 'p_form': profile_form}
        return render(self.request, 'registration/update-profile.html', context)

    def post(self, *args, **kwargs):
        user_form = UserUpdate(self.request.POST, instance=self.request.user)
        profile_form = ProfileUpdate(self.request.POST, self.request.FILES, instance=self.request.user.profile)
        context = {'u_form': user_form, 'p_form': profile_form}
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(self.request, 'Profile updated!')
            return redirect('profile')
        else:
            messages.warning(self.request, 'Correct the errors below.')
            return redirect('profile_update')
        return render(self.request, 'registration/update-profile.html', context)