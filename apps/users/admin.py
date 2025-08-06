from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AuditLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display  = ('email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter   = ('role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering      = ('email',)
    fieldsets     = (
        (None,           {'fields': ('email', 'password')}),
        ('Personal Info',{'fields': ('first_name', 'last_name')}),
        ('Permissions',  {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name','role','password1','password2'),
        }),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'path', 'method', 'ip_address')
    list_filter  = ('action', 'user__role')
    search_fields = ('user__email', 'action', 'path')
    ordering     = ('-timestamp',)