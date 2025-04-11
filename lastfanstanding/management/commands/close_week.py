from django.core.management.base import BaseCommand
from django.utils import timezone
from lastfanstanding.models import LFSGame, LFSPick

class Command(BaseCommand):
    help = "Closes current week of LFS"

    def handle(self, *args, **options):
        # do something
        print(f"Closing week: Increment week number, check which teams won and lost on the picks")
        current_game = LFSGame.objects.get(year=2025)
        newweek = current_game.current_week + 1
        current_game.current_week = newweek
        current_game.save()