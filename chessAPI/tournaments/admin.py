from django.contrib import admin
from .models import *


class TournamentAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Tournament', {'fields': ['name', 'start', 'end', 'place']}),
        ('Game details', {'fields': ['game_rate', 'game_system', 'is_polish_rated', 'game_type', 'round_number']}),
        ('Organizer', {'fields': ['judge', 'organizer']}),
        (None, {'fields': ['is_started', 'is_ended']}),
        ('Description', {'fields': ['description']}),
    ]
    list_filter = ['start']
    list_display = ('name', 'start')


class TournamentMemberAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['person', 'tournament', 'points', 'title', 'fide_rating']}),
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
    list_display = ('round', 'chessboard', 'white', 'black')


class PromotionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['participant', 'title', 'status']}),
    ]
    list_display = ('participant', 'title', 'status')
    list_filter = ('status',)


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TournamentMember, TournamentMemberAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Promotion, PromotionAdmin)
