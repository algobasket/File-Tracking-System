from functools import wraps
from django.shortcuts import redirect

def check_session_exists(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'role' not in request.session:
            # Session doesn't exist, redirect to logout page or perform logout
            return redirect('logout')  # Redirect to logout URL
        return view_func(request, *args, **kwargs)
    return wrapper