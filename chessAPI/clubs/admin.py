from django.contrib import admin
from .models import *


class ClubAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'email', 'registration', 'manager', 'address']}),
    ]
    list_display = ('name', 'email', 'registration', 'manager')
    list_filter = ('name', )


admin.site.register(Club, ClubAdmin)
