from django.contrib import admin
from .models import AuditLog, RequestLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "content_type", "object_id")
    list_filter = ("action", "user", "content_type")
    search_fields = ("object_repr", "changes")
    date_hierarchy = "timestamp"
    readonly_fields = [f.name for f in AuditLog._meta.fields]


@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "method", "path", "status_code", "duration_ms")
    list_filter = ("method", "status_code", "user")
    search_fields = ("path", "ip_address", "user_agent")
    date_hierarchy = "timestamp"
    readonly_fields = [f.name for f in RequestLog._meta.fields]