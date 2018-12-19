from django import forms
from naccbis.models import TeamIds, LeagueOffenseOverall


class MyForm(forms.Form):
    team_choices = [("ALL", "All Teams")] + [(team.id, team.name) for team in TeamIds.objects.using('data').all()]
    team = forms.ChoiceField(choices=team_choices)
    min_pa = forms.ChoiceField(choices=[(x, x) for x in range(0, 126, 25)])
    season_choices = [("ALL", "All Seasons")] + [(x.season, x.season) for x in LeagueOffenseOverall.objects.using('data').order_by('-season')]
    season = forms.ChoiceField(choices=season_choices)
