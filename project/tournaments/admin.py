from django.contrib import admin
from .models import *


class TournamentAdmin(admin.ModelAdmin):
    def address(self, obj):
        return obj.address.province + obj.address.city

    fieldsets = [
        ('Tournament', {'fields': ['name', 'start', 'end', 'address']}),
        ('Game details', {'fields': ['game_rate', 'game_system', 'is_fide', 'game_type']}),
        ('Organizer', {'fields': ['judge', 'organizer']})
    ]
    list_filter = ['start']
    list_display = ('name', 'start')


class AddressAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Address', {'fields': ['country', 'province', 'city', 'street', 'house_number']})
    ]
    list_filter = ['country', 'province']
    list_display = ('country', 'province', 'city', 'street')


class TournamentApplicationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['person', 'tournament']})
    ]

    list_display = ('person', 'tournament')


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(TournamentApplication, TournamentApplicationAdmin)
