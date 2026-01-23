from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def cs_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/accounts/login/")
        if not getattr(request.user, "is_cs", False):
            return HttpResponseForbidden("Customer Service access required.")
        return view_func(request, *args, **kwargs)
    return _wrapped
