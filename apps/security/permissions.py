from rest_framework.permissions import BasePermission
from django.core.exceptions import ImproperlyConfigured


class IsSuperUser(BasePermission):
    """
    Allows access only to Django superusers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class HasModelPermission(BasePermission):
    """
    Checks 'app_label.action_model' against user permissions.
    e.g. 'patients.add_patient', 'billing.view_invoice'
    """

    def has_permission(self, request, view):
     model = getattr(view, "queryset", None) and view.queryset.model
     if model is None:
         raise ImproperlyConfigured(
            f"{view.__class__.__name__} must set `.queryset` or `.get_queryset()`."
        )
     model_name = model._meta.model_name  # e.g. 'patient'
     perm = f"{model._meta.app_label}.{self._action_map[request.method].format(model=model_name)}"
     return request.user.has_perm(perm)
 

    _action_map = {
        "GET": "view_{model}",
        "POST": "add_{model}",
        "PUT": "change_{model}",
        "PATCH": "change_{model}",
        "DELETE": "delete_{model}",
    }

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)