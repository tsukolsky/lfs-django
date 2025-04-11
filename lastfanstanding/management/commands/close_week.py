from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils import timezone
from lastfanstanding.models import LFSGame, LFSPick

class Command(BaseCommand):
    help = "Closes current week of LFS if the criteria is met"

    def handle(self, *args, **options):
        """
        # First, get the current LFS game and see what week it is
        # Based on the week, this needs to do a few things
        # 1) Close out teams that are now closed out, if they were not already. This script should be called frequently,
             so it cannot just update the week/clouseouts every time it is called. It needs to assess the current date
             and make sure it's still with in the week. once sunday 1300 hits, the next week can roll over.
        """

        """
        You can call a command from python using the call_command(<command string>)
        For example, to call this command would be call_command('close_week')
        """
        print(f"Closing week: Increment week number, check which teams won and lost on the picks")
        current_game = LFSGame.objects.get(year=2025)
        newweek = current_game.current_week + 1
        current_game.current_week = newweek
        current_game.save()