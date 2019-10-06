from django.urls import path

from naccbis.views import LeaderboardView, TeamOffenseView

urlpatterns = [
    path('leaders/batters', LeaderboardView.as_view()),
    path('leaders/team_offense', TeamOffenseView.as_view()),
]
