from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def role_required(*required_roles):
    """
    Restrict access to users with one of the specified roles.
    Usage:
        @role_required("student")
        @role_required("instructor", "employee")
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login_view')
            if request.user.role not in required_roles:
                return HttpResponseForbidden("You do not have access to this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
