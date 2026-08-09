from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import Http404


def yum_required(view_func):
    """Restricts a view to an authenticated superuser (the site owner)."""

    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404
        return view_func(request, *args, **kwargs)

    return wrapped
