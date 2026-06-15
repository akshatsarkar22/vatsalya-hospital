from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def staff_required(view_func):
    """Require login and staff/superuser access for HMS dashboard views."""
    @wraps(view_func)
    @login_required(login_url='/login/')
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'You do not have permission to access the dashboard.')
        return redirect('home')
    return _wrapped_view
