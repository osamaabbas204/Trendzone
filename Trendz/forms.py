from django.core import validators
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contact


# create Forms here

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'class': 'form-control', 'placeholder': 'you@email.com'}),
            'message': forms.Textarea(attrs={'class': 'textarea', 'class': 'form-control md-textarea', 'rows': '6', 'placeholder': 'Your message...'}),
        }


class CreateUserForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "input",
        'class': 'form-control',
        "placeholder": "enter password"
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "input",
        'class': 'form-control',
        "placeholder": "re-enter password"
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input', 'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'input', 'class': 'form-control', 'placeholder': 'you@email.com'}),
        }
