from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.utils import timezone


import random

STAGECHOICES = [
    ('O', 'Octavos de final'),
    ('Q', 'Cuartos de final'),
    ('SF', 'Semifinales'),
    ('F', 'Final'),
]

REGIONCHOICES=[
        ('NA','NA'),
        ('EU','EU'),
        ('AP','AP'),
        ('KR','KR'),
]

STATUSCHOICES=[
        ('open','open'),
        ('in progress','in progress'),
        ('completed','completed'),
]

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

class Team(models.Model):
    name = models.CharField(max_length=100)
    player1 = models.ForeignKey(User, related_name='team_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(User, related_name='team_player2', on_delete=models.CASCADE)
    player3 = models.ForeignKey(User, related_name='team_player3', on_delete=models.CASCADE)
    player4 = models.ForeignKey(User, related_name='team_player4', on_delete=models.CASCADE)
    player5 = models.ForeignKey(User, related_name='team_player5', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100)
    teams = models.ManyToManyField(Team)
    status = models.CharField(max_length=20, choices=STATUSCHOICES, default='open')
    winner = models.ForeignKey(Team, related_name='tournament_winner', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    def round_of_8(self):
        # Obtener los equipos del torneo
        teams = self.teams.all()
        # Verificar que hayan exactamente 8 equipos
        if len(teams) != 8:
            return None
        # Mezclar los equipos aleatoriamente
        shuffled_teams = list(teams)
        random.shuffle(shuffled_teams)
        # Crear los partidos para la ronda de cuartos
        matches = [self.create_match(shuffled_teams[i], shuffled_teams[i+1], 'Q') for i in range(0, 8, 2)]
        return matches

    def round_of_4(self):
        # Obtener los equipos ganadores de la ronda de cuartos
        winning_teams = [match.winner for match in self.match_set.filter(round='Q')]
        # Verificar que hayan exactamente 4 equipos ganadores
        if len(winning_teams) != 4:
            return None
        # Mezclar los equipos aleatoriamente
        shuffled_teams = list(winning_teams)
        random.shuffle(shuffled_teams)
        # Crear los partidos para la ronda de semifinales
        matches = [self.create_match(shuffled_teams[i], shuffled_teams[i+1], 'SF') for i in range(0, 4, 2)]
        return matches

    def round_of_2(self):
        # Obtener los equipos ganadores de la ronda de semifinales
        winning_teams = [match.winner for match in self.match_set.filter(round='SF')]
        # Verificar que hayan exactamente 2 equipos ganadores
        if len(winning_teams) != 2:
            return None
        # Mezclar los equipos aleatoriamente
        shuffled_teams = list(winning_teams)
        random.shuffle(shuffled_teams)
        # Crear el partido para la final
        match = self.create_match(shuffled_teams[0], shuffled_teams[1], 'F')
        return [match]

    def final(self):
        # Obtener el equipo ganador del torneo
        return self.winner

class Match(models.Model):
    tournament = models.ForeignKey(Tournament, related_name='matches', on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, related_name='team1_matches', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_matches', on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, related_name='won_matches')
    stage = models.CharField(max_length=2, choices=STAGECHOICES, default='O')

    def play(self):
        # Aquí iría la lógica para jugar un partido entre dos equipos
        # y determinar quién gana.
        team1 = self.team1
        team2 = self.team2
        return team1 if random.choice([True, False]) else team2

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    def accept(self):
        self.accepted_at = timezone.now()
        self.save()

    def reject(self):
        self.delete()

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    is_online = models.BooleanField(blank=True,default=False)
    looking_for_group = models.BooleanField(blank=True,default=False)

    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    valorantName = models.TextField(max_length=20, blank=True)
    valorantTagline = models.TextField(max_length=7, blank=True)
    valorantRegion = models.TextField(blank=True, choices=REGIONCHOICES)
    valorantLeague = models.TextField(max_length=40, blank=True)
    valorantRangue = models.TextField(max_length=40, blank=True)
    valorantCurrentRR = models.TextField(max_length=40, blank=True)
    valorantCalculatedElo = models.TextField(max_length=40, blank=True)
    valorantKills = models.TextField(max_length=40, blank=True)
    valorantDeaths = models.TextField(max_length=40, blank=True)
    valorantAssists = models.TextField(max_length=40, blank=True)
    valorantBodyshots = models.TextField(max_length=40, blank=True)
    valorantHeadshots = models.TextField(max_length=40, blank=True)
    friends = models.ManyToManyField(User, related_name='friends')
    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    def get_absolute_url(self):
        print("entro¿¿")
        return "/"