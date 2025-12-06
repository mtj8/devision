from django.urls import path
from .views import (
    InitView,
    LoginView,
    SignupView,
    UserHackathonsView,
    UserPastHackathonsView,
    UserFriendsView,
    HackathonSearchView,
    HackathonLeaderboardView,
    UserLookupView,
    UserHistoryView,
    TeamLookupView,
    TeamHistoryView,
)


urlpatterns = [
    path("init/", InitView.as_view(), name="init"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("user/hackathons", UserHackathonsView.as_view(), name="user-hackathons"),
    path("user/past-hackathons", UserPastHackathonsView.as_view(), name="user-past-hackathons"),
    path("user/friends", UserFriendsView.as_view(), name="user-friends"),
    path("hackathons", HackathonSearchView.as_view(), name="hackathon-search"),
    path("hackathon/<uuid:hackathon_id>/leaderboard", HackathonLeaderboardView.as_view(), name="hackathon-leaderboard"),
    path("user/lookup", UserLookupView.as_view(), name="user-lookup"),
    path("user/lookup/<uuid:user_id>/history", UserHistoryView.as_view(), name="user-history"),
    path("team/lookup", TeamLookupView.as_view(), name="team-lookup"),
    path("team/<uuid:team_id>/history", TeamHistoryView.as_view(), name="team-history"),
]

