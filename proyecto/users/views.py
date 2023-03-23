from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm, TournamentForm,MessageForm
from .forms import EditProfileForm
from .forms import TeamForm
from users.models import Match, Profile,FriendRequest, Team, Tournament, Message
from django.views.generic.edit import UpdateView
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden,HttpResponseBadRequest
import random
import requests
import json
from django.db.models import Q


@login_required
def simulate_match(request, tournament_id, match_id):
    tournament = Tournament.objects.get(id=tournament_id)
    matches = Match.objects.filter(tournament=tournament, winner__isnull=True)


    winners = []
    for match in matches:
        score1 = int(request.POST.get(f'score1_{match.id}'))
        score2 = int(request.POST.get(f'score2_{match.id}'))

        # Actualizamos el score del partido
        match.score1 = score1
        match.score2 = score2
        match.save()

        # Simulamos el partido y actualizamos el ganador
        if score1 > score2:
            match.winner = match.team1
            winners.append(match.team1)
        elif score2 > score1:
            match.winner = match.team2
            winners.append(match.team2)
        else:
            match.winner = None
        match.save()
    tournament.teams.set(winners)
    tournament.save()
    context = {
        'tournament': tournament,
        'matches': matches,
        'winners': winners
    }

    return render(request, 'users/tournament_matches.html', context)

@login_required
def tournament_matches(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    matches = Match.objects.filter(tournament=tournament)

    if request.method == 'POST':
        for match in matches:
            score1 = int(request.POST['score1_' + str(match.id)])
            score2 = int(request.POST['score2_' + str(match.id)])
            match.score1 = score1
            match.score2 = score2
            match.save()
            

        # Redirigir al usuario de vuelta a la página de partidos del torneo
        return redirect('tournament_matches', tournament_id=tournament_id)

    context = {'tournament': tournament, 'matches': matches}
    return render(request, 'users/tournament_matches.html', context)

@login_required
def messages(request, username=None):
    user = request.user
    if username:
        other_user = get_object_or_404(User, username=username)
        messages = Message.objects.filter(sender=user, recipient=other_user).order_by('date_sent') | Message.objects.filter(sender=other_user, recipient=user)
    else:
        other_user = None
        messages = Message.objects.filter(recipient=user)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            message.recipient = other_user
            message.save()
            return redirect('messages')
    else:
        form = MessageForm()

    users = User.objects.exclude(id=user.id)

    return render(request, 'users/messages.html', {'users': users, 'messages': messages, 'other_user': other_user, 'form': form})

@login_required
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    matches = []
    if(3<tournament.teams.count()<5):
       
        #entramos a semis.
        teams = list(tournament.teams.all())
        match1 = Match(team1=teams[0], team2=teams[1], tournament_id=tournament.id)
        match2 = Match(team1=teams[2], team2=teams[3], tournament_id=tournament.id)
        match1.save()
        match2.save()
        matches.append(match1)
        matches.append(match2)
    elif(2<tournament.teams.count()<3):
        teams = list(tournament.teams.all())
        match1 = Match(team1=teams[0], team2=teams[1], tournament_id=tournament.id)
        match1.save()
        matches.append(match1)
        print(match1)
    elif(tournament.teams.count()==1):
        teams = list(tournament.teams.all())
        tournament.winner=teams[0]
        tournament.status='completed'
        tournament.save()

        print("pablo maricon y roman bujarra")
    context = {'tournament': tournament, 'matches': matches}
    return render(request, 'users/tournament_detail.html', context)

@login_required
def tournaments_list(request):
    tournaments = Tournament.objects.all()
    context = {'tournaments': tournaments}
    return render(request, 'users/tournaments_list.html', context)

@login_required
def tournament_results(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    matches = Match.objects.filter(tournament_id=tournament_id)
    rounds = {
        'quarterfinals': [[team.name for team in match] for match in matches.filter(stage='Q')],
        'semifinals': [[team.name for team in match] for match in matches.filter(stage='S')],
        'final': [team.name for team in matches.filter(stage='F')],
    }
    context = {'tournament': tournament, 'rounds': rounds}
    return render(request, 'users/tournaments_results.html', context)



@login_required
def create_tournament(request):
    if request.method == 'POST':
        form = TournamentForm(request.POST)
        if form.is_valid():
            # Obtener los valores de los campos del formulario
            name = form.cleaned_data['name']
            teams = form.cleaned_data['teams']
            if len(teams) != 8:
                form.add_error('teams', 'The tournament must have exactly 8 teams')
                return render(request, 'users/create_tournament.html', {'form': form})

            # Crear el torneo y las relaciones con los equipos
            tournament = Tournament(name=name)
            tournament.save()
            tournament.teams.set(teams)

            # Obtener los equipos y barajarlos
            teams = list(tournament.teams.all())
            random.shuffle(teams)

            matches = []
            for i in range(0, len(teams), 2):
                match = Match(team1=teams[i], team2=teams[i+1], tournament_id=tournament.id)
                match.save()
                matches.append(match)

            while len(matches) > 1:
                winners = []
                for i in range(0, len(matches), 2):
                    match1 = matches[i]
                    match2 = matches[i+1]
                    winner = play_match(match1, match2)
                    winners.append(winner)

                if len(winners) == 1:
                    # Si solo queda un equipo, es el ganador del torneo
                    break

                matches = winners

            # Mostrar los resultados del torneo
            rounds = {
                'quarterfinals': [[team.name for team in match.teams.all()] for match in tournament.matches.filter(stage='Q')],
                'semifinals': [[team.name for team in match.teams.all()] for match in tournament.matches.filter(stage='S')],
                'final': [team.name for team in tournament.matches.filter(stage='F')],
            }

            context = {'tournament': tournament, 'rounds': rounds}
            return render(request, 'users/create_tournament.html', context)
    else:
        form = TournamentForm()

    return render(request, 'users/create_tournament.html', {'form': form})


def play_match(team1, team2):
    # Aquí iría la lógica para jugar un partido entre dos equipos
    # y determinar quién gana. Por ejemplo, podrías generar un
    # resultado aleatorio o utilizar algún algoritmo más sofisticado.
    # En este ejemplo, simplemente se devuelve uno de los equipos al azar.
    return team1 if random.choice([True, False]) else team2

def match_detail(request, match_id):
    match = Match.objects.get(id=match_id)
    if request.method == 'POST':
        match.winner = play_match(match.team1, match.team2)
        match.save()
    return render(request, 'users/match_detail.html', {'match': match})


@login_required
def create_team(request):
    form = TeamForm()
    if request.method == 'POST':
        form = TeamForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        username_players = [form.cleaned_data[f'player{i}'] for i in range(1, 6)]
        players = []
        existing_players = []
        for username in username_players:
            try:
                player = User.objects.get(username=username)
                if Team.objects.filter(Q(player1=player) | Q(player2=player) | Q(player3=player) | Q(player4=player) | Q(player5=player)).exists():
                    existing_players.append(player)
                else:
                    players.append(player)
            except User.DoesNotExist:
                form.add_error(f'player{len(players)+1}', f'The user "{username}" does not exist')

        if existing_players:
            players_str = ', '.join([str(player) for player in existing_players])
            form.add_error(None, f'The following players already belong to a team: {players_str}. Please select other players.')
        elif len(players) < 5:
            form.add_error(None, 'Please select five players for the team.')
        else:
            team = Team.objects.create(name=name, player1=players[0], player2=players[1], player3=players[2], player4=players[3], player5=players[4])
            team.player1 = players[0]
            team.player2 = players[1]
            team.player3 = players[2]
            team.player4 = players[3]
            team.player5 = players[4]
            team.save()
            return redirect('home')
    return render(request, 'users/create_team.html', {'form': form})

@login_required
def players_looking_for_group_on_your_elo(request):
    eloAux = request.user.profile.valorantCalculatedElo
    intElo = int(eloAux)
    users = list(User.objects.exclude(profile__valorantCalculatedElo="").exclude(profile=None).exclude(username=request.user.username))
    friends = request.user.profile.friends.all()
    filtered_users = []
    contador = 0
    for usuario in users:
        print(usuario.profile.valorantCalculatedElo)
        eloBucleAux = int(usuario.profile.valorantCalculatedElo)
        print(eloBucleAux)
        booleanoAux = (abs(eloBucleAux - intElo) < 100)
        booleanoAux2 = bool(usuario.profile.looking_for_group)
        booleanoAux3 = bool(usuario.profile.is_online)##booleano 3 is online, meter dentro del  and
        if booleanoAux and booleanoAux2 and booleanoAux3:
            filtered_users.append(usuario)
            contador=contador+1
    context = {'users': filtered_users}
    context.update({'cont': contador})
    context.update({'friends': friends })
    return render(request, 'users/players_looking_for_group_on_your_elo.html', context)

def users_list(request):
    users = User.objects.all().order_by('profile__valorantCalculatedElo')
    userCont = list(User.objects.all())
    usersConnected = list(User.objects.exclude(profile__is_online=False))
    useraux = request.user
    friendsaux = useraux.profile.friends.all()
    
    context = {'users': users}
    context.update({'friends': friendsaux})
    context.update({'userContInt': len(userCont)})
    context.update({'usersOnline': len(usersConnected)})
    context.update({'useraux': useraux})

    return render(request, 'users/users_list.html', context)

@login_required
def accept_friend_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id)
    if request.user != friend_request.receiver:
        return HttpResponseForbidden()
    friend_request.accept()
    friend_request.receiver.profile.friends.add(friend_request.sender)
    friend_request.sender.profile.friends.add(friend_request.receiver)
    request.user.save()
    FriendRequest.delete(friend_request)
    return redirect('friends_list')



@login_required
def reject_friend_request(request, friend_request_id):
    friend_request = get_object_or_404(FriendRequest, id=friend_request_id)
    print("holaaaaaaaa")
    print(friend_request_id)
    parseintid=int(friend_request_id)
    context = {'idDelete': parseintid}
    return render(request, 'users/friends_list.html',context)

@login_required
def friends_list(request):
    user = request.user
    friends = user.profile.friends.all()
    context = {'friends': friends}
    return render(request, 'users/friends_list.html',context)#preguntar como hacer la redirección

@login_required
def add_friend(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    if(request.user.profile.id == friend_id):
        return HttpResponseBadRequest("Cant add yourself as a friend")
    else:
        friend_request, created = FriendRequest.objects.get_or_create(sender=request.user, receiver=friend)

    if not created:
        return redirect('users_list') # La solicitud ya existe
    return redirect('users_list')

@login_required
def delete_friend(request, friend_id):
    user = request.user
    friend_user = get_object_or_404(User, id=friend_id)
    user.profile.friends.remove(friend_user)
    friend_user.profile.friends.remove(user)
    user.save()
    friend_user.save()
    return redirect('friends_list')


"""
    friend = User.objects.get(id=friend_id)
    request.user.profile.friends.add(friend)
    request.user.save()
    friend_id=friend.profile.id + 1
    print(friend_id)
    friend.profile.friends.add(User.objects.get(id=request.user.profile.id))
    #friend to me, a partir de friend
    # saco el usuario con un get id del user
    #
    return redirect('profile', pk=request.user.profile.pk)
"""
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
        userAux.profile.is_online = True
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

def looking_for_group(request):
    userGet=request.user
    userGet.profile.looking_for_group=True
    userGet.save()
    return render(request, 'users/home.html') 

def stop_looking_for_group(request):
    userGet=request.user
    userGet.profile.looking_for_group=False
    userGet.save()
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
            
        if(range == ""):
            range=0
        

        calculatedElo=calculatedElo+int(range)*33+int(currentRR)
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
