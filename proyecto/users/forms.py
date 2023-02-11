from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput
REGIONCHOICES=[
        ('NA','NA'),
        ('EU','EU'),
        ('AP','AP'),
        ('KR','KR'),
]
class SignupForm(UserCreationForm):

    first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.')
    birth_date = forms.DateTimeField(widget=DateInput, help_text='Required. Format: YYYY-MM-DD')
    valorantName = forms.CharField(max_length=20, required=True, help_text='Required. Enter your valorantname.')
    valorantRegion = forms.CharField(required=True, widget=forms.Select(choices=REGIONCHOICES))
    valorantTagline = forms.CharField(max_length=3, required=True, help_text='Required. Enter your tagline. Format: AAA')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'password1', 'password2','valorantName','valorantRegion','valorantTagline')