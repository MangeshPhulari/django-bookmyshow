# users/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile # <-- Import the new Profile model

class UserRegisterForm(UserCreationForm):
    """
    A form for user registration that includes an email field.
    It inherits from UserCreationForm to handle secure password hashing.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email'] # The password fields are handled automatically by the parent form.


class UserUpdateForm(forms.ModelForm):
    """
    A form for updating a user's username and email.
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# --- ADD THIS NEW FORM ---
class ProfileUpdateForm(forms.ModelForm):
    """
    A form for updating a user's profile picture.
    """
    class Meta:
        model = Profile
        fields = ['image']