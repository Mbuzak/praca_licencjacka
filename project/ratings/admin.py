from django.contrib import admin
from .models import *


class PolishRatingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['name', 'person', 'obtain', 'tournament']}),
    )

    list_filter = ['name']
    list_display = ['name', 'person', 'obtain', 'tournament']


class FideRatingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Osoba', {'fields': ['person']}),
        ('Ranking', {'fields': ['classic', 'rapid', 'blitz']}),
    )

    list_filter = ['person']
    list_display = ['person', 'classic', 'rapid', 'blitz']


class FidePeriodAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Data', {'fields': ['change', 'month', 'year']}),
    )

    list_filter = ['month', 'year']
    list_display = ['change', 'month', 'year']


class FideHistoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Osoba', {'fields': ['person']}),
        ('Data', {'fields': ['period']}),
        ('Ranking', {'fields': ['classic', 'rapid', 'blitz']}),
    )

    list_filter = ['person']
    list_display = ['person', 'classic', 'rapid', 'blitz']


admin.site.register(PolishRating, PolishRatingAdmin)
admin.site.register(FideRating, FideRatingAdmin)
admin.site.register(FideHistory, FideHistoryAdmin)
admin.site.register(FidePeriod, FidePeriodAdmin)
