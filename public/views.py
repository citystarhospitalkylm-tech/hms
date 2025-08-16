from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.http import Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from functools import wraps
from apps.appointments.models import Appointment
from django.contrib.sessions.models import Session
from apps.patients.models import Patient
from apps.billing.models import Invoice
from apps.consultations.models import Consultation, Prescription
from apps.labs.models import LabOrder

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

# --- Decorator ---
def role_required(role_slug):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if getattr(request.user, "is_superuser", False):
                return view_func(request, *args, **kwargs)

            user_role = getattr(request.user, "role", None)
            if not user_role and request.user.groups.exists():
                user_role = request.user.groups.first().name
            user_role = (user_role or "").strip().lower()

            if user_role != role_slug.strip().lower():
                return HttpResponseForbidden("You do not have permission to view this page.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# --- Landing & Login ---
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
            request.session["login_role"] = role
            login(request, user)
            return redirect(ROLE_REDIRECTS[role])
        return render(request, "registration/login.html", {"role": role, "error": "Invalid credentials"})

    return render(request, "registration/login.html", {"role": role})

# --- Dashboards ---
@role_required("admin")
def admin_dashboard(request):
    User = get_user_model()
    now = timezone.now()
    recent_users = User.objects.exclude(last_login=None).order_by("-last_login")[:5]

    context = {
        "role": "Admin",
        "user_count": User.objects.count(),
        "active_sessions": Session.objects.filter(expire_date__gt=now).count(),
        "module_count": len(ROLES),
        "recent_users": recent_users,
    }
    return render(request, "dashboard_admin.html", context)

@role_required("doctor")
def doctor_dashboard(request):
    upcoming = Appointment.objects.select_related("patient", "doctor")\
                                   .filter(doctor=request.user, appointment_time__gte=timezone.now())\
                                   .order_by("appointment_time")[:5]
    context = {
        "role": "Doctor",
        "patient_count": Patient.objects.count(),
        "upcoming_appointments": upcoming,
    }
    return render(request, "dashboard_doctor.html", context)

@role_required("nurse")
def nurse_dashboard(request):
    # If assigned nurse relation exists, filter by it. Else show all patients.
    assigned = getattr(Patient.objects, "all")().order_by("first_name")[:5]
    context = {
        "role": "Nurse",
        "assigned_patients": assigned,
    }
    return render(request, "dashboard_nurse.html", context)

@role_required("pharmacy")
def pharmacy_dashboard(request):
    pending = Prescription.objects.select_related("patient", "prescribed_by")\
                                  .filter(items__isnull=False).distinct()[:5]
    context = {
        "role": "Pharmacy",
        "pending_prescriptions": pending,
    }
    return render(request, "dashboard_pharmacy.html", context)

@role_required("lab")
def lab_dashboard(request):
    pending = LabOrder.objects.select_related("patient", "test")\
                               .filter(status=LabOrder.Status.ORDERED)[:5]
    context = {
        "role": "Laboratory",
        "pending_tests": pending,
    }
    return render(request, "dashboard_lab.html", context)

@role_required("appointments")
def appointments_dashboard(request):
    upcoming = Appointment.objects.select_related("patient", "doctor")\
                                   .filter(appointment_time__gte=timezone.now())\
                                   .order_by("appointment_time")[:10]
    context = {
        "role": "Appointments",
        "upcoming": upcoming,
    }
    return render(request, "dashboard_appointments.html", context)

@role_required("billing")
def billing_dashboard(request):
    outstanding = Invoice.objects.select_related("patient")\
                                 .filter(status__in=[Invoice.Status.DRAFT, Invoice.Status.PARTIALLY_PAID, Invoice.Status.OVERDUE])[:5]
    context = {
        "role": "Billing",
        "outstanding_invoices": outstanding,
    }
    return render(request, "dashboard_billing.html", context)

@role_required("consultations")
def consultations_dashboard(request):
    recent = Consultation.objects.select_related("patient", "doctor").order_by("-scheduled_at")[:5]
    context = {
        "role": "Consultations",
        "recent_consults": recent,
    }
    return render(request, "dashboard_consultations.html", context)