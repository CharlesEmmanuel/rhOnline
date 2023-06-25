from django.shortcuts import redirect
from employe.models import Employe


def employe_permission(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 'AD':

            return view_func(request, *args, **kwargs)
        else:
            # Redirigez l'utilisateur vers une page d'erreur ou effectuez une autre action appropriée.
            return redirect('dashboard')

    return wrapper


def delete_permission(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superadmin == True:

            return view_func(request, *args, **kwargs)
        else:
            # Redirigez l'utilisateur vers une page d'erreur ou effectuez une autre action appropriée.
            return redirect('dashboard')

    return wrapper


def show_permission(request, pk):
    try:
        employe = Employe.objects.get(id=pk)
        account = employe.account
        if request.user.is_authenticated and request.user.is_admin:
            return request.user.is_authenticated
        else:
            return request.user.is_authenticated and request.user == account
    except Employe.DoesNotExist:
        return False
