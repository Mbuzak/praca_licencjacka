from django.contrib import admin
from .models import *


class AddressAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Address', {'fields': ['province', 'city', 'street', 'house_number']})
    ]
    list_filter = ['province']
    list_display = ('province', 'city', 'street')


admin.site.register(Address, AddressAdmin)
