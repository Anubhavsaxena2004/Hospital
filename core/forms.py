from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    department = forms.CharField(max_length=100, required=False)
    specialization = forms.CharField(max_length=100, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role', 
                 'department', 'specialization', 'phone_number')
