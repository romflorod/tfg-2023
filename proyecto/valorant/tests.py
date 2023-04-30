from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile,Team, Tournament, Match
from django.urls import reverse

class UserTestCase(TestCase):
    "testing user"
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
        )
        self.user_profile = self.user.profile
        
    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, "testuser")
        
    def test_user_profile_email(self):      
        self.assertEqual(self.user_profile.user.email, "")  

    
    def test_username(self):
        self.assertEqual(self.user.username, "testuser")
        
    def test_email(self):
        self.user.email = "testuser@example.com"
        self.assertEqual(self.user.email, "testuser@example.com")

    def test_password(self):
        self.assertTrue(self.user.check_password("testpass"))
        
class AuthenticationTest(TestCase):
    "testing authentication"   
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
        )

    def test_login(self):
        response = self.client.post('/login/', {
            "username": "testuser",
            "password": "testpass",
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/", status_code=302, target_status_code=302)
   
    def test_login_invalid_username(self):
        response = self.client.post('/login/', {
            "username": "invaliduser",
            "password": "testpass",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")
    def test_login_invalid_password(self):
        response = self.client.post('/login/', {
            "username": "testuser",
            "password": "invalidpass",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")


class TeamTest(TestCase):
    "testing equipos"
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        self.user3 = User.objects.create_user(username='testuser3', password='testpass123')
        self.user4 = User.objects.create_user(username='testuser4', password='testpass123')
        self.user5 = User.objects.create_user(username='testuser5', password='testpass123')

        self.team = Team.objects.create(name='Test Team',
                                        player1=self.user1,
                                        player2=self.user2,
                                        player3=self.user3,
                                        player4=self.user4,
                                        player5=self.user5)

    def test_team_creation(self):
        self.assertEqual(self.team.__str__(), 'Test Team')
    
        
    def test_team_player_names(self):
        self.assertEqual(self.team.player1.username, 'testuser1')
        self.assertEqual(self.team.player2.username, 'testuser2')
        self.assertEqual(self.team.player3.username, 'testuser3')
        self.assertEqual(self.team.player4.username, 'testuser4')
        self.assertEqual(self.team.player5.username, 'testuser5')
    def test_team_player_change(self):
        self.team.player1 = self.user5
        self.assertEqual(self.team.player1.username, 'testuser5')
        
class TournamentTest(TestCase):
    "testing torneo"
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        self.user3 = User.objects.create_user(username='testuser3', password='testpass123')
        self.user4 = User.objects.create_user(username='testuser4', password='testpass123')
        self.user5 = User.objects.create_user(username='testuser5', password='testpass123')

        self.team1 = Team.objects.create(name='Test Team 1',
                                        player1=self.user1,
                                        player2=self.user2,
                                        player3=self.user3,
                                        player4=self.user4,
                                        player5=self.user5)

        self.team2 = Team.objects.create(name='Test Team 2',
                                        player1=self.user1,
                                        player2=self.user2,
                                        player3=self.user3,
                                        player4=self.user4,
                                        player5=self.user5)

        self.tournament = Tournament.objects.create(name='Test Tournament')
        self.tournament.teams.add(self.team1)
        self.tournament.teams.add(self.team2)

    def test_tournament_creation(self):
        self.assertEqual(self.tournament.__str__(), 'Test Tournament')

    def test_tournament_teams(self):
        self.assertEqual(self.tournament.teams.count(), 2)
        self.assertIn(self.team1, self.tournament.teams.all())
        self.assertIn(self.team2, self.tournament.teams.all())

    def test_remove_team_from_tournament(self):
        self.tournament.remove_team(self.team1)
        self.assertEqual(self.tournament.teams.count(), 1)
        self.assertNotIn(self.team1, self.tournament.teams.all())
        self.assertIn(self.team2, self.tournament.teams.all())
        
class MatchTestCase(TestCase):
    "testing para crear matches"
    def setUp(self):
        # Creamos 4 usuarios para crear los equipos
        self.user1 = User.objects.create_user(username='user1', password='pass1')
        self.user2 = User.objects.create_user(username='user2', password='pass2')
        self.user3 = User.objects.create_user(username='user3', password='pass3')
        self.user4 = User.objects.create_user(username='user4', password='pass4')

        # Creamos 2 equipos para realizar los partidos
        self.team1 = Team.objects.create(
            name='Team 1',
            player1=self.user1,
            player2=self.user2,
            player3=self.user3,
            player4=self.user4,
            player5=self.user1,
        )

        self.team2 = Team.objects.create(
            name='Team 2',
            player1=self.user2,
            player2=self.user3,
            player3=self.user4,
            player4=self.user1,
            player5=self.user2,
        )

        # Creamos un torneo
        self.tournament = Tournament.objects.create(name='Tournament')
        self.tournament.teams.set([self.team1, self.team2])

        # Creamos un partido para el torneo
        self.match = Match.objects.create(
            tournament=self.tournament,
            team1=self.team1,
            team2=self.team2,
        )

    def test_play(self):
        """
        Test que comprueba que el método play del modelo Match funciona correctamente
        """
        winner = self.match.play()
        self.assertIn(winner, [self.team1, self.team2])
        self.assertNotEqual(winner, None)
        
    def test_team1_score(self):
        """
        Test que comprueba que el equipo 1 tiene un marcador inicial de 0
        """
        self.assertEqual(self.match.score1, None)
        
    def test_team2_score(self):
        """
        Test que comprueba que el equipo 2 tiene un marcador inicial de 0
        """
        self.assertEqual(self.match.score2, None)
        
    def test_stage_is_saved(self):
        """
        Test que comprueba que la etapa del partido se guarda correctamente
        """
        self.assertEqual(self.match.stage, 'O')
        self.match.stage = 'F'
        self.match.save()
        self.assertEqual(self.match.stage, 'F')