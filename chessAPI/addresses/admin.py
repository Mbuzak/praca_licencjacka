from django.contrib import admin
from .models import *

'''
class AddressAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Address', {'fields': ['province', 'city', 'street']})
    ]
    list_filter = ['province']
    list_display = ('province', 'city', 'street')


admin.site.register(Address, AddressAdmin)
'''