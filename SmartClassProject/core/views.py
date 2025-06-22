from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Profile

# 🔹 SIGNUP VIEW
from django.db import IntegrityError
from .models import Profile

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        user_type = request.POST.get('user_type')
        print("User type received:", user_type)

        if user_type:
            user_type = user_type.capitalize().strip()

        if form.is_valid() and user_type in ['Student', 'Teacher']:
            try:
                user = form.save()
                # ✅ Check if profile already exists
                profile, created = Profile.objects.get_or_create(user=user)
                profile.user_type = user_type
                profile.save()

                login(request, user)
                print("✅ Registration successful. Redirecting to /success/")
                return redirect('success')
            except IntegrityError as e:
                print("❌ IntegrityError:", str(e))
                form.add_error(None, "A problem occurred during profile creation.")
        else:
            print("❌ Form is invalid or user_type is incorrect.")
            print(form.errors)

    else:
        form = UserCreationForm()

    return render(request, 'core/signup.html', {'form': form})




# 🔹 LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            try:
                profile = Profile.objects.get(user=user)
                user_type = profile.user_type.lower()

                if user_type == 'student':
                    return redirect('student_dashboard')
                elif user_type == 'teacher':
                    return redirect('teacher_dashboard')
                else:
                    return redirect('unknown_role')
            except Profile.DoesNotExist:
                return redirect('unknown_role')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


# 🔹 SUCCESS PAGE
def success_view(request):
    return render(request, 'core/success.html')


# 🔹 DASHBOARDS
@login_required
def student_dashboard_view(request):
    return render(request, 'core/student_dashboard.html')


@login_required
def teacher_dashboard_view(request):
    return render(request, 'core/teacher_dashboard.html')


@login_required
def unknown_role_view(request):
    return render(request, 'core/unknown_role.html')
