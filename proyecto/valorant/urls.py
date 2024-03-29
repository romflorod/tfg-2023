"""valorant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('signup/', user_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('profile/<int:pk>',  user_views.profile, name='profile'),
    path('looking_for_group',  user_views.looking_for_group, name='looking_for_group'),
    path('stop_looking_for_group',  user_views.stop_looking_for_group, name='stop_looking_for_group'),
    path('players_looking_for_group_on_your_elo/', user_views.players_looking_for_group_on_your_elo, name='players_looking_for_group_on_your_elo'),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    path('terms/', user_views.TermsView.as_view(template_name="users/terms.html"), name='terms'),
    path('add_friend/<int:friend_id>', user_views.add_friend, name='add_friend'),
    path('delete_friend/<int:friend_id>', user_views.delete_friend, name='delete_friend'),
    path('friends_list/', user_views.friends_list, name='friends_list'),
    path('accept_friend_request/<int:friend_request_id>/', user_views.accept_friend_request, name='accept_friend_request'),
    path('reject-friend-request/<int:friend_request_id>/', user_views.reject_friend_request, name='reject_friend_request'),  
    path('messages/', user_views.messages, name='messages'),
    path('messages/<str:username>/', user_views.messages, name='messages'),
    path('profile/editprofile/<int:pk>', user_views.editprofile, name='editprofile'),
    path('users_list/', user_views.users_list, name='users_list'),
    path('create_team/', user_views.create_team, name='create_team'),
    path('create_tournament/', user_views.create_tournament, name='create_tournament'),
    path('tournaments_results/<int:tournament_id>/', user_views.tournament_results, name='tournaments_results'),
    path('tournaments_list/', user_views.tournaments_list, name='tournaments_list'),
    path('tournaments_list/', user_views.tournaments_list, name='tournaments_list'),
    path('tournament/<int:tournament_id>/', user_views.tournament_detail, name='tournament_detail'),
    path('tournament_matches/<int:tournament_id>/', user_views.tournament_matches, name='tournament_matches'),
    path('<int:tournament_id>/simulate_match/<int:match_id>/', user_views.simulate_match, name='simulate_match'),
    path('match/<int:match_id>/', user_views.match_detail, name='match_detail'),
    ]

urlpatterns+= staticfiles_urlpatterns()