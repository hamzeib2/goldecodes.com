from django.http import HttpResponse
from django.shortcuts import redirect

def unauth_user(view_func):
    def wrapper_func(request , *args ,**kwargs):
        if request.user.is_authenticated:
            return redirect('store')
        else:
            return view_func(request , *args ,**kwargs)
    return wrapper_func

def auth_user(view_func):
    def wrapper_func(request , *args ,**kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        else:
            return view_func(request , *args ,**kwargs)
    return wrapper_func

def allowed_users(allowed_roles= []):
    def decorator(view_func): 
        def wrapper_func(request , *args ,**kwargs):
            groub = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

                print(group)
            if group in allowed_roles:
                return view_func(request , *args ,**kwargs)
            else:
                return HttpResponse('you are not authorized to view this page')
        return wrapper_func
    return decorator
