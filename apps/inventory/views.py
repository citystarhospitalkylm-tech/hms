from django.shortcuts import render
from config.rbac import require_module

@require_module("inventory")
def inventory_dashboard(request):
    return render(request, "inventory/dashboard.html")