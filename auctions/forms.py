from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import User

class EditProfileForm(UserChangeForm):
    password = None  # Exclude the password field from being edited

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  # Add fields you'd like the user to be able to edit
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
