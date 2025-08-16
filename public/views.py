from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps

ROLES = [
    {"name": "Admin",         "slug": "admin"},
    {"name": "Doctor",        "slug": "doctor"},
    {"name": "Nurse",         "slug": "nurse"},
    {"name": "Pharmacy",      "slug": "pharmacy"},
    {"name": "Laboratory",    "slug": "lab"},
    {"name": "Appointments",  "slug": "appointments"},
    {"name": "Billing",       "slug": "billing"},
    {"name": "Consultations", "slug": "consultations"},
]

ROLE_REDIRECTS = {r["slug"]: f"/dashboard/{r['slug']}/" for r in ROLES}

# Decorator to enforce matching role
def role_required(role_slug):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user_role = getattr(request.user, "role", None)
            # Fall back to staff groups if you don’t have a `role` field:
            if not user_role and request.user.groups.exists():
                user_role = request.user.groups.first().name.lower()
            if user_role != role_slug:
                return HttpResponseForbidden("You do not have permission to view this page.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def landing_page(request):
    return render(request, "landing.html", {"roles": ROLES})

def role_login(request, role):
    role = role.lower()
    if role not in ROLE_REDIRECTS:
        raise Http404("Invalid role")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            # Optionally: store the selected role in session for quick checks
            request.session["login_role"] = role
            login(request, user)
            return redirect(ROLE_REDIRECTS[role])
        return render(request, "login.html", {"role": role, "error": "Invalid credentials"})

    return render(request, "login.html", {"role": role})

# Now each dashboard is locked to its role
@role_required("admin")
def admin_dashboard(request):
    return render(request, "dashboard_placeholder.html", {"role": "Admin"})

@role_required("doctor")
def doctor_dashboard(request):
    return render(request, "dashboard_placeholder.html", {"role": "Doctor"})

@role_required("nurse")
def nurse_dashboard(request):
    return render(request, "dashboard_placeholder.html", {"role": "Nurse"})

@role_required("pharmacy")
def pharmacy_dashboard(request):
    return render(request, "dashboard_placeholder.html", {"role": "Pharmacy"})

@role_required("lab")
def lab_dashboard(request):
    return render(request, "dashboard_placeholder.html", {"role": "Laboratory"})

@role_required("appointments")
def appointments_dashboard(request):
    return render(request, "dashboard_placeholder.html", {"role": "Appointments"})

@role_required("billing")
def billing_dashboard(request):
    return render(request, "dashboard_placeholder.html", {"role": "Billing"})

@role_required("consultations")
def consultations_dashboard(request):
    return render(request, "dashboard_placeholder.html", {"role": "Consultations"})