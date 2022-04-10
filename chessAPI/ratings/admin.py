from django.contrib import admin
from .models import *


class FideRatingAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Osoba', {'fields': ['person', 'fide_number']}),
        ('Ranking', {'fields': ['classic', 'rapid', 'blitz']}),
    )

    list_filter = ['person']
    list_display = ['person', 'fide_number', 'classic', 'rapid', 'blitz']


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


admin.site.register(FideRating, FideRatingAdmin)
admin.site.register(FideHistory, FideHistoryAdmin)
admin.site.register(FidePeriod, FidePeriodAdmin)
