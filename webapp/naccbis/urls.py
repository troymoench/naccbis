from django.urls import path

from naccbis.views import LeaderboardView

urlpatterns = [
    path('', LeaderboardView.as_view()),
]
