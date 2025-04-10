from django.shortcuts import render
from django.http import HttpResponse
from .models import LFSTeam, LFSGame
from django.template import loader


# Create your views here.
MIN_WEEK = 1

def index(request):
    # This page should show:
    # # A title bar with:
    #   the total number of teams still alive aka "Active"
    #   The total pot size
    # # A list of teams (active) and their picks up to the current week.

    # Get current game - this should be done by year
    current_game = LFSGame.objects.get(year=2025)
    # Get current teams associated with this year - for this view, it should only be the active teams
    lfs_teams = current_game.lfsteam_set.filter(active=True)

    # Need to provide the list of picks for all the teams in order to iterate over them and create
    # a valid table. For each LFS Team, you can get the picks with lfs_teams[i].lfspick_set.all().
    # This could be passed in as a dictionary, then list?
    # TODO: Make this code great again, because its very dirty. Something to do with tags?
    # TODO: look here https://stackoverflow.com/questions/2894365/use-variable-as-dictionary-key-in-django-template
    team_pick_dictionary = {}
    if current_game.current_week > MIN_WEEK:
        for week in range(MIN_WEEK, current_game.current_week):
            team_pick_dictionary[week] = [] # Should contain LFS Team and NFL team name of the pick

        for team in lfs_teams:
            team_picks = team.lfspick_set.all()
            # This pick dictionary should now contain the week number as key, and image directory as the value
            for pick in team_picks:
                value = (pick.lfs_team.team_name, pick.nfl_team.name) # TODO: update nfl_team.name to nfl_icon path
                team_pick_dictionary[pick.nfl_week].append(value)

    lfs_potsize = current_game.CalculatePotSize(lfs_teams)
    current_game.pot_size = lfs_potsize
    current_game.total_teams = len(lfs_teams)
    current_game.save()

    template = loader.get_template("lastfanstanding/index.html")
    context = {
        "lfs_team_list": lfs_teams,
        "lfs_pot_size": lfs_potsize,
        "lfs_game_week": current_game.current_week-1,
        "week_range" : list(range(MIN_WEEK, current_game.current_week)),
        "lfs_team_picks": team_pick_dictionary,
    }
    return HttpResponse(template.render(context, request))

def teaminfo(request, teamname):
    return HttpResponse(f"You are looking at team info for team {teamname}")

def userhomepage(request, username):
    return HttpResponse(f"You are looking at the homepage for user {username}")

def picker(request, username):
    return HttpResponse(f"You are looking at the weekly picker for user {username}")
