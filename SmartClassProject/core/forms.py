from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomSignupForm(UserCreationForm):
    USER_TYPES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')
