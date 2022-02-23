from django.contrib import admin
from .models import PolishRating


class PolishRatingAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['name', 'person', 'obtain', 'tournament']}),
    )

    list_filter = ['name']
    list_display = ['name', 'person', 'obtain', 'tournament']


admin.site.register(PolishRating, PolishRatingAdmin)
