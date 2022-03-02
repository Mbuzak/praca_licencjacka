from django.contrib import admin
from .models import *


class TournamentAdmin(admin.ModelAdmin):
    def address(self, obj):
        return obj.address.province + obj.address.city

    fieldsets = [
        ('Tournament', {'fields': ['name', 'start', 'end', 'address']}),
        ('Game details', {'fields': ['game_rate', 'game_system', 'is_fide', 'game_type', 'round_count']}),
        ('Organizer', {'fields': ['judge', 'organizer']})
    ]
    list_filter = ['start']
    list_display = ('name', 'start')


class TournamentApplicationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['person', 'tournament']})
    ]

    list_display = ('person', 'tournament')


class TournamentMemberAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['person', 'tournament']})
    ]

    list_display = ('person', 'tournament')


class RoundAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['tournament', 'round']})
    ]

    list_display = ('tournament', 'round')


class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['round', 'chessboard', 'white', 'black', 'white_result', 'black_result']})
    ]

    list_display = ('round', 'chessboard', 'white', 'black', 'white_result', 'black_result')


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentApplication, TournamentApplicationAdmin)
admin.site.register(TournamentMember, TournamentMemberAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Round, RoundAdmin)
