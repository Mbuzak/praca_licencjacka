from django.contrib import admin
from .models import *


class ClubAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'email', 'address', 'registration', 'manager']})
    ]
    list_display = ('name', 'email', 'address', 'registration', 'manager')
    list_filter = ('name', )


class ClubApplicationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['club', 'person']})
    ]
    list_display = ('club', 'person')


class ClubMemberAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['club', 'person']})
    ]
    list_display = ('club', 'person')


admin.site.register(Club, ClubAdmin)
admin.site.register(ClubApplication, ClubApplicationAdmin)
admin.site.register(ClubMember, ClubMemberAdmin)
