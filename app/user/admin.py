from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from user.models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'last_login', 'is_admin',)
    search_fields = ('email', 'username',)
    readonly_fields = ('id', 'last_login',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_per_page = 10


admin.site.register(User, UserAdmin)
