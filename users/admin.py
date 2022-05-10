from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdminConfig(UserAdmin):
    model = Account
    list_display = ('email', 'id','username', )

admin.site.register(Account, AccountAdminConfig)