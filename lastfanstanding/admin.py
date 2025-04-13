from django.contrib import admin

# Register your models here.
from .models import LFSTeam, NFLTeam, LFSPick, LFSGame

admin.site.register(NFLTeam)
admin.site.register(LFSTeam)
admin.site.register(LFSGame)
admin.site.register(LFSPick)