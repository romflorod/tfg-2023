from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from users.models import Profile
from django.views.generic.edit import UpdateView
class EditProfileView(UpdateView):
    model = Profile
    template_name = 'editprofile.html'
    fields = ['birth_date','valorantName','valorantRegion','valorantTagline']

def home(request):
    return render(request, 'users/home.html')
    
def profile(request):
    return render(request, 'users/profile.html')

def getStatsCustom(auxList):
    import requests
    url= "https://api.kyroskoh.xyz/valorant/v1/mmr/"+auxList[0]+"/"+auxList[1]+"/"+auxList[2]+""
    stat= requests.get(url).text
    stat.strip
    stataux=stat.split("-")
    leagueAndRangue=stataux[0]
    currentRR=stataux[1]#RR ACTUALES
    leagueAndRangueAux=leagueAndRangue.split(" ")
    league=leagueAndRangueAux[0]#LIGAS: BRONCE SILVER GOLD PLATINUM DIAMANOND ASCENDANT INMORTAL ASCENDANT
    range=leagueAndRangueAux[1]#RANGOS: 1, 2, 3 PER LEAGUE
    calculatedElo= 0;
    if(league=="Bronce"):
        calculatedElo=calculatedElo+100
    if(league=="Silver"):
        calculatedElo=calculatedElo+200
    if(league=="Gold"):
        calculatedElo=calculatedElo=+300
    if(league=="Platinum"):
        calculatedElo=calculatedElo+400
    if(league=="Diamond"):
        calculatedElo=calculatedElo+500
    if(league=="Ascendant"):
        calculatedElo=calculatedElo+600
    if(league=="Inmortal"):
        calculatedElo=calculatedElo+700
    if(league=="Radiant"):
        calculatedElo=calculatedElo+800
    calculatedElo=calculatedElo+int(range)+int(currentRR.replace("RR.",""))         
    statlist=[league,range,currentRR,calculatedElo]
    return statlist
 
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
            auxList=[form.cleaned_data.get('valorantRegion'),form.cleaned_data.get('valorantName'),form.cleaned_data.get('valorantTagline')]
            stats=getStatsCustom(auxList)
            user.profile.valorantLeague=stats[0]
            user.profile.valorantRangue=stats[1]
            user.profile.valorantCurrentRR=stats[2]
            user.profile.valorantCalculatedElo=stats[3]
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
