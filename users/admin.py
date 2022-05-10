from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile



class AccountAdminConfig(UserAdmin):
    model = Account
    list_display = ('email', 'id','username', )
    exclude = ('date_joined','last_login',)

admin.site.register(Account)
admin.site.register(UserProfile)