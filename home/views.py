from django.shortcuts import render, redirect
from django.contrib import messages, auth

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.
@login_required(login_url="login")
def dashboard(request):
    print("this is user")
    print(auth.get_user(request))
    return render(request, 'dashboard/menu.html')


def login_user(request):
    # breakpoint()
    if request.method == 'POST':

        if not request.POST['email_utilisateur'] and not request.POST['password_utilisateur']:

            messages.error(request, "Connexion Echouée", "danger")
        else:

            email = request.POST['email_utilisateur']
            password = request.POST['password_utilisateur']

            # Calcul de la durée de contrat
            # print("Email :", email, " mot de passe",password)
            user = auth.authenticate(email=email, password=password)
            if (user is not None):
                print("Connecté")
                auth.login(request, user)
                # return redirect("dashboard")
                return render(request, 'dashboard/menu.html')
            else:
                print("Non Connecté")
                messages.error(request, "Connexion Echouée", "danger")
                return redirect("login")

    return render(request, 'home/login.html')


def logout_view(request):
    logout(request)
    # return render(request, 'home/login.html')
    return redirect('login')


def pointage_page(request):
    return render(request, 'home/pointage.html')
    # return redirect('home')


# def home_page(request):
#     return render(request, 'home/home.html')


def entry(request):
    return render(request, 'home/entree.html')


def sortie(request):
    return render(request, 'home/sortie.html')
