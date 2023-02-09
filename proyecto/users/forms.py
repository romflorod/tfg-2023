from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    valorantName = forms.CharField(max_length=20, required=True, help_text='Required. Enter your valorantname.')
    valorantTagline = forms.CharField(max_length=4, required=True, help_text='Required. Enter your tagline. Format: AAA')
    valorantRegion = forms.CharField(max_length=3, required=True, help_text='Required. na, eu, ap, kr. Format: AA')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'password1', 'password2','valorantName','valorantTagline','valorantRegion')