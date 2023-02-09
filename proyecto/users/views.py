from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm

def home(request):
    return render(request, 'users/home.html')

def profile(request):
    return render(request, 'users/profile.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.valorantName = form.cleaned_data.get('valorantName')
            user.profile.valorantTagline = form.cleaned_data.get('valorantTagline')
            user.profile.valorantRegion = form.cleaned_data.get('valorantRegion')
            user.profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.save()

            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
        
    context = { 'form': form }
    return render(request, 'users/signup.html', context)
