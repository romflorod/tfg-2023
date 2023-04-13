from datetime import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from users.models import Profile, Tournament,Message
from users.models import Team
from django.utils import timezone
from django.forms import DateInput

REGIONCHOICES=[
        ('NA','NA'),
        ('EU','EU'),
        ('AP','AP'),
        ('KR','KR'),
]
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('content',)
class TournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'teams']

    name = forms.CharField(max_length=100)
    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), widget=forms.CheckboxSelectMultiple)

    def clean_teams(self):
        teams = self.cleaned_data.get('teams')
        if len(teams) != 8:
            raise forms.ValidationError("You must select exactly 8 teams.")
        return teams

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'player1', 'player2', 'player3', 'player4', 'player5')

class DateInput(forms.DateInput):
    input_type = 'date'

class EditProfileForm(UserChangeForm):

    #first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    #last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    #email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.')
    birth_date = forms.DateTimeField(widget=DateInput, help_text='Required. Format: YYYY-MM-DD')
    valorantName = forms.CharField(max_length=20, required=True, help_text='Required. Enter your valorantname.')
    valorantRegion = forms.CharField(required=True, widget=forms.Select(choices=REGIONCHOICES))
    valorantTagline = forms.CharField(max_length=7, required=True, help_text='Required. Enter your tagline. Format: AAA')
    

    class Meta:
        model = Profile
        fields = ('birth_date','valorantName','valorantRegion','valorantTagline')

    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date'].date()
        age = (timezone.now().date() - birth_date).days // 365 # Calcular edad en años
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        if birth_date > timezone.now():
            raise forms.ValidationError("Birth date cannot be in the future.")
        return birth_date
     
class SignupForm(UserCreationForm):

    first_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=50, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=120, help_text='Required. Enter a valid email address.')
    birth_date = forms.DateTimeField(widget=DateInput, help_text='Required. Format: YYYY-MM-DD')
    valorantName = forms.CharField(max_length=20, required=True, help_text='Required. Enter your valorantname.')
    valorantRegion = forms.CharField(required=True, widget=forms.Select(choices=REGIONCHOICES))
    valorantTagline = forms.CharField(max_length=7, required=True, help_text='Required. Enter your tagline. Format: AAA')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'birth_date', 'password1', 'password2','valorantName','valorantRegion','valorantTagline')
    
    def clean_birth_date(self):
        birth_date = self.cleaned_data['birth_date'].date()
        age = (timezone.now().date() - birth_date).days // 365 # Calcular edad en años
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register.")
        if birth_date > timezone.now():
            raise forms.ValidationError("Birth date cannot be in the future.")
        return birth_date