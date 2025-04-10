from email.policy import default

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# Need to enumerate NFL Teams

class LFSGame(models.Model):
    year = models.IntegerField(default=2025)
    pot_size = models.IntegerField(default=0)
    total_teams = models.IntegerField(default=0)
    current_week = models.IntegerField(default=1)

    def IncrementWeek(self):
        self. current_week += 1

    def CalculatePotSize(self, lfs_teams : list) -> int:
        """
        Takes in a list of LFSTeams
        """
        total_pot = 0
        for team in lfs_teams:
            if team.paid_intitial:
                total_pot += 15
            if team.paid_buyback:
                total_pot += 10
        return total_pot

    def __str__(self):
        return (f"{self.year}, pot_size=${self.pot_size}, total_teams={self.total_teams}, "
                f"current_week={self.current_week}")

class NFLTeam(models.Model):
    name = models.CharField(max_length=32)
    icon_path = models.CharField(max_length=128)
    bye_week = models.PositiveIntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(18)]) # between 1 and 18

    def __str__(self):
        return f"{self.name}, bye_week={self.bye_week}, icon_path={self.icon_path}"

class LFSUser(models.Model):
    user_email = models.EmailField()
    last_login = models.DateTimeField("last login")

    def __str__(self):
        return f"{self.user_email}, last_login= {self.last_login}"

class LFSTeam(models.Model):
    team_name = models.CharField(max_length=64)
    lfs_user = models.ForeignKey(LFSUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    paid_buyback = models.BooleanField(default=False)
    paid_intitial = models.BooleanField(default=False)
    lfs_game = models.ForeignKey(LFSGame, on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.team_name}, active={self.active}, paid_initial={self.paid_intitial}, "
                f"paid_buyback={self.paid_buyback}, user={self.lfs_user}")

class LFSPick(models.Model):
    nfl_week = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(18)])
    nfl_team = models.ForeignKey(NFLTeam, on_delete=models.CASCADE)
    lfs_team = models.ForeignKey(LFSTeam, on_delete=models.CASCADE)
    win_loss = models.BooleanField()

    def __str__(self):
        return f"pk={self.pk}, team={self.nfl_team}, nfl_week={self.nfl_week}, team={self.lfs_team}, win_loss={self.win_loss}"