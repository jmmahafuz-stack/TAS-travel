from functools import wraps
from django.shortcuts import redirect


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if getattr(request.user, 'role', '') != 'admin':
            # Non-admins go to their appropriate dashboard
            if getattr(request.user, 'role', '') == 'user':
                return redirect('user_dashboard')
            return redirect('MyTrip')
        return view_func(request, *args, **kwargs)

    return _wrapped


def user_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if getattr(request.user, 'role', '') != 'user':
            # Admins should be redirected to the Django admin site
            if getattr(request.user, 'role', '') == 'admin':
                return redirect('admin:index')
            return redirect('MyTrip')
        return view_func(request, *args, **kwargs)

    return _wrapped
