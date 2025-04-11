from django.shortcuts import render
from django.http import HttpResponse
from .models import LFSTeam, LFSGame, LFSPick
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

    # Create a tuple list that contains the (lfs_team, its picks). The picks should be sorted by week to match the
    # columns
    lfs_teams_tuple_list = []
    for team in lfs_teams:
        team_picks = team.lfspick_set.all().order_by("nfl_week")
        lfs_teams_tuple_list.append((team, team_picks))

    # Calculate pot size and save to the game
    lfs_potsize = current_game.CalculatePotSize(lfs_teams)
    current_game.pot_size = lfs_potsize
    current_game.total_teams = len(lfs_teams)
    current_game.save()

    # Calculate the tops picks for this week - this should be the top five of all teams
    this_week_picks = LFSPick.objects.filter(nfl_week=current_game.current_week-1)
    topPicks = {}
    for pick in this_week_picks:
        if pick.nfl_team.name in topPicks:
            topPicks[pick.nfl_team.name] += 1
        else:
            topPicks[pick.nfl_team.name] = 1

    sorted_top_picks = dict(sorted(topPicks.items(), key=lambda item: item[1], reverse=True))
    top_keys = list(sorted_top_picks.keys())
    numRankings = min(len(top_keys),5)
    top_picks_tuples = [ (team_name, topPicks[team_name]) for team_name in top_keys[0:numRankings]]

    # Load template
    template = loader.get_template("lastfanstanding/index.html")
    context = {
        "lfs_team_list": lfs_teams_tuple_list,
        "lfs_pot_size": lfs_potsize,
        "lfs_game_week": current_game.current_week-1,
        "week_range" : list(range(MIN_WEEK, current_game.current_week)),
        "top_picks" : top_picks_tuples,
    }
    return HttpResponse(template.render(context, request))

def teaminfo(request, teamname):
    return HttpResponse(f"You are looking at team info for team {teamname}")

def userhomepage(request, username):
    return HttpResponse(f"You are looking at the homepage for user {username}")

def picker(request, username):
    return HttpResponse(f"You are looking at the weekly picker for user {username}")
