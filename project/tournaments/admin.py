from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *


class TournamentAdmin(admin.ModelAdmin):
    def address(self, obj):
        return obj.address.province + obj.address.city

    fieldsets = [
        ('Tournament', {'fields': ['name', 'start', 'end', 'address']}),
        ('Game details', {'fields': ['game_rate', 'gameplay', 'is_fide']}),
        ('Organizer', {'fields': ['id_judge', 'organizer']})
    ]
    list_filter = ['start']
    list_display = ('name', 'start')


class AddressAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Address', {'fields': ['country', 'province', 'city', 'street', 'house_number']})
    ]
    list_filter = ['country', 'province']
    list_display = ('country', 'province', 'city', 'street')


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Address, AddressAdmin)
