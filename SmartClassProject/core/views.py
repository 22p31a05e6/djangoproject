from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .models import Profile
from django.db import IntegrityError

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        user_type = request.POST.get('user_type')
        if form.is_valid() and user_type:
            try:
                user = form.save()
                # Avoid duplicate Profile creation
                Profile.objects.get_or_create(user=user, defaults={'user_type': user_type})
                login(request, user)
                return redirect('success')
            except IntegrityError:
                form.add_error(None, "An account with this profile already exists.")
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('success')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def success_view(request):
    return render(request, 'core/success.html')
