from django import forms
from naccbisapp.models import TeamIds, LeagueOffenseOverall


class BattersInputs(forms.Form):
    team_choices = [("ALL", "All Teams")] + \
                   [(team.id, team.name) for team in TeamIds.objects.all()]
    team = forms.ChoiceField(choices=team_choices)
    min_pa = forms.ChoiceField(choices=[(x, x) for x in range(0, 126, 25)])
    season_choices = [("ALL", "All Seasons")] + \
                     [(x.season, x.season) for x in LeagueOffenseOverall.objects.order_by('-season')]
    season = forms.ChoiceField(choices=season_choices)
    split = forms.ChoiceField(choices=[("ALL", "Overall"), ("CONF", "Conference")])
    stat = forms.ChoiceField(choices=[("DB", "Dashboard"),
                                      ("STD", "Standard"),
                                      ("ADV", "Advanced")])


class TeamOffenseInputs(forms.Form):
    season_choices = [("ALL", "All Seasons")] + \
                     [(x.season, x.season) for x in LeagueOffenseOverall.objects.order_by('-season')]
    season = forms.ChoiceField(choices=season_choices)
    split = forms.ChoiceField(choices=[("ALL", "Overall"), ("CONF", "Conference")])
    stat = forms.ChoiceField(choices=[("DB", "Dashboard"),
                                      ("STD", "Standard"),
                                      ("ADV", "Advanced")])
