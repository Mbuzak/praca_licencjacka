from django.contrib import admin
from .models import Account
from .forms import EditProfileForm, RegisterForm


class AccountAdmin(admin.ModelAdmin):
    form = EditProfileForm
    add_form = RegisterForm
    list_display = ('email', 'title', 'name', 'lastname', 'born_year')
    list_filter = ()
    fieldsets = [
        (None, {'fields': ('email', 'name', 'lastname', 'gender', 'born_year', 'club')}),
        ('Address', {'fields': ('province',)}),
        ('Title', {'fields': ('title',)}),
    ]
    filter_horizontal = ('groups', 'user_permissions')
    search_fields = ('email',)


admin.site.register(Account, AccountAdmin)
