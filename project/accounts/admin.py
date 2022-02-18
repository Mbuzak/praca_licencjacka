from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Account
from accounts.forms import EditProfileForm, RegisterForm


class AccountAdmin(admin.ModelAdmin):
    form = EditProfileForm
    add_form = RegisterForm
    list_display = ('email', 'name', 'lastname', 'born_year')
    list_filter = ()
    fieldsets = [
        (None, {'fields': ('email', 'name', 'lastname', 'born_year')}),
    ]

    search_fields = ('email',)


admin.site.register(Account, AccountAdmin)  # TBD -> AUTH_USER_MODEL
