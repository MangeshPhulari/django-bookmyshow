# users/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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

# The 'ProfileUpdateForm' has been removed. Password changes should be handled
# by Django's built-in auth views (PasswordChangeView, PasswordResetView)
# which use secure forms like 'PasswordChangeForm'.
#
# In your profile.html, you correctly link to the password reset flow:
# <a href="{% url 'password_reset' %}" ...>Reset Password</a>
# This is the correct and secure way to handle it.