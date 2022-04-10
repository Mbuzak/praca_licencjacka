from django.contrib import admin
from .models import Application


class ApplicationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['type_of_object', 'person', 'club', 'tournament']})
    ]
    list_display = ('type_of_object', 'person', 'club', 'tournament')
    list_filter = ('type_of_object',)


admin.site.register(Application, ApplicationAdmin)
