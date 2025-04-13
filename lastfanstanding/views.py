from django.shortcuts import render
from django.http import HttpResponse
from .models import LFSTeam, LFSGame, LFSPick
from django.template import loader
from datetime import datetime, timedelta
from .forms import TeamPickerForm

# Create your views here.
MIN_WEEK = 1

def index(request):
    print(f"User is authenticated {request.user.is_authenticated}")
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

    top_keys = list(dict(sorted(topPicks.items(), key=lambda item: item[1], reverse=True)).keys())
    numRankings = min(len(top_keys),5)
    top_picks_string = ""
    for team_name in top_keys[0:numRankings]:
        top_picks_string += f"{team_name}: {topPicks[team_name]}, "
    top_picks_string = top_picks_string[:-2]

    # Get countdown clocks ready for the countdown timers for current picks
    timeremaining = datetime(2025,4,13,13, 0, 0) - datetime.now()
    if (timeremaining.total_seconds() < 0):
        timeremaining = timedelta(0)
    hours = timeremaining.days * 24 + timeremaining.seconds//3600
    print(f"time remaining {timeremaining}\nseconds { timeremaining.seconds}, hours {hours}")
    endDate = {'hours' : hours,
               'minutes' : (timeremaining.seconds  % 3600) // 60,
               'seconds' : timeremaining.seconds  % 60
               }

    # Load template
    template = loader.get_template("lastfanstanding/index.html")
    context = {
        "user" : request.user,
        "lfs_team_list": lfs_teams_tuple_list,
        "lfs_pot_size": lfs_potsize,
        "lfs_game_week": current_game.current_week,
        "week_range" : list(range(MIN_WEEK, current_game.current_week)),
        "top_picks" : top_picks_string,
        "end_date" : endDate,
    }
    return render(request, "lastfanstanding/index.html", context)

def chooseteam(request):
    if request.method == 'POST':
        form = TeamPickerForm(request.POST)
        if form.is_valid():
            # process the data
            pass
    else:
        form = TeamPickerForm()
    context = { "form" : form, "user " : request.user,}
    return render(request, "lastfanstanding/chooseteam.html", context)

def userhomepage(request, username):
    context = { "user " : request.user,}
    return HttpResponse(f"You are looking at the homepage for user {username}")

def rules(request):
    context = { "user " : request.user,}
    return render(request, "lastfanstanding/rules.html", context)

def cheapseats(request):
    # Get current game - this should be done by year
    current_game = LFSGame.objects.get(year=2025)

    # Get current teams associated with this year - for this view, it should only be the active teams
    lfs_teams = current_game.lfsteam_set.filter(active=False)

    # Create a tuple list that contains the (lfs_team, its picks). The picks should be sorted by week to match the
    # columns
    lfs_teams_tuple_list = []
    for team in lfs_teams:
        team_picks = team.lfspick_set.all().order_by("nfl_week")
        lfs_teams_tuple_list.append((team, team_picks))

    context = {
        "user " : request.user,
        "lfs_inactive_teams" : lfs_teams_tuple_list
    }
    return render(request, "lastfanstanding/cheapseats.html", context)
