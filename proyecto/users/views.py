from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from .forms import EditProfileForm
from users.models import Profile
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
import requests
import json

class EditProfileView(UpdateView):
    model = Profile
    template_name = 'editprofile.html'
    fields = ['birth_date','valorantName','valorantRegion','valorantTagline']
    Form = EditProfileForm

class TermsView(ListView):
    model = Profile
    template_name = "terms.html"

def home(request):
    userAux=request.user
    if(userAux.is_authenticated):
        auxList=[userAux.profile.valorantRegion,userAux.profile.valorantName,userAux.profile.valorantTagline]
        stats=getStatsCustom(auxList)
        userAux.refresh_from_db()
        userAux.profile.valorantLeague=stats[0]
        userAux.profile.valorantRangue=stats[1]
        userAux.profile.valorantCurrentRR=stats[2]
        userAux.profile.valorantCalculatedElo=stats[3]
        userAux.profile.valorantKills=stats[4]
        userAux.profile.valorantDeaths=stats[5]
        userAux.profile.valorantAssists=stats[6]
        userAux.profile.valorantBodyshots=stats[7]
        userAux.profile.valorantHeadshots=stats[8]        
        userAux.profile.save()    
        if userAux.profile.valorantLeague == "error":
            form = EditProfileForm()
            context = { 'form': form }
            return redirect("profile/editprofile/"+str(userAux.profile.id))                           
    return render(request, 'users/home.html')
    
def profile(request,pk):
    userGet=request.user
    context={}
    if (userGet.is_authenticated):
        return render(request, 'users/profile.html', context)
    else:
        return render(request, 'users/home.html')

   



def getStatsCustom(auxList):
    url= "https://api.kyroskoh.xyz/valorant/v1/mmr/"+auxList[0]+"/"+auxList[1]+"/"+auxList[2]+""
    url2="https://api.henrikdev.xyz/valorant/v3/matches/"+auxList[0]+"/"+auxList[1]+"/"+auxList[2]+""
    requestHENRIK=(requests.get(url2))
    if(requestHENRIK.status_code==200 and requests.get(url).status_code==200):
        jsonRequest= json.dumps(requestHENRIK.json())
        requestJsonBruta=jsonRequest.split("kills")
        requestJsonBrutaLimIzqAux=requestJsonBruta[1]
        requestJsonBrutaLimIzq=requestJsonBrutaLimIzqAux.split("legshots")
        requestJsonFina=requestJsonBrutaLimIzq[0].replace('"','').replace(":","")
        requestJsonFinaSplit=requestJsonFina.split(",")
        valorantKills=int(requestJsonFinaSplit[0].strip())
        valorantDeaths=int(requestJsonFinaSplit[1].replace("deaths","").strip())
        valorantAssists=int(requestJsonFinaSplit[2].replace("assists","").strip())
        valorantBodyshots=int(requestJsonFinaSplit[3].replace("bodyshots","").strip())
        valorantHeadshots=int(requestJsonFinaSplit[4].replace("headshots","").strip())
        stat= requests.get(url).text
        stat.strip()
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
        if("null" in currentRR):
            currentRR="0RR"
        if("RR." in currentRR):
            currentRR=currentRR.replace("RR.","")
        if("RR" in currentRR):
            currentRR=currentRR.replace("RR","")     
        calculatedElo=calculatedElo+int(range)+int(currentRR)
        statlist=[league,range,currentRR,calculatedElo,valorantKills,valorantDeaths,valorantAssists,valorantBodyshots,valorantHeadshots]
    else:
        statlist=["error",0,0,0,0,0,0,0,0]
   

    return statlist
 

def editprofile(request, pk):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            profile = Profile.objects.get(id=pk)
            user = profile.user
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
            user.profile.valorantKills=stats[4]
            user.profile.valorantDeaths=stats[5]
            user.profile.valorantAssists=stats[6]
            user.profile.valorantBodyshots=stats[7]
            user.profile.valorantHeadshots=stats[8]

            user.profile.save()
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            user.save()
        
            return redirect('/profile/'+str(pk) )
    else:
        form = EditProfileForm()
    context = { 'form': form }
    return render(request, 'users/editprofile.html', context)

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
            user.profile.valorantKills=stats[4]
            user.profile.valorantDeaths=stats[5]
            user.profile.valorantAssists=stats[6]
            user.profile.valorantBodyshots=stats[7]
            user.profile.valorantHeadshots=stats[8]
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
