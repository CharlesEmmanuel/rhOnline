from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib import messages

from sinistre.models import Employe
from sinistre.models import Sinistre
# from django.contrib.auth.decorators import login_required


def liste_empl(request):
    employe_list = Employe.objects.filter(soft_deleting=False)
    context = {
        'listing': employe_list
    }
    return render(request, 'sinistre/liste_emp.html', context)


def add_sinistre(request, pk):
    try:
        employe = Employe.objects.get(id=pk)

    except employe.DoesNotExist:
        messages.success(request, "Employé n'existe pas")

    if request.method == 'POST':

        if not request.POST['sinistreype'] and not request.POST['debutsinistre']:

            messages.error(request, "Ajout de sinistre Échouée", "danger")
        else:

            typesinistre = request.POST['sinistreype']
            datedebut = request.POST['debutsinistre']
            datefin = request.POST['finsinistre']
            salairemp = request.POST['paye']
            missionemp = request.POST['role']

            # Calcul de la durée de sinistre

            sinistre = Sinistre()

            sinistre.typesinistre = typesinistre
            sinistre.mission = missionemp

            sinistre.datedebut = datedebut
            sinistre.datefin = datefin
            sinistre.salaire = salairemp
            sinistre.employe_id = employe.pk

            sinistre.save()

            # Code d'ajout du sinistre

            messages.success(request, "sinistre Enrégistré", "success")
            return redirect('sinistre_liste_emp')
    else:
        context = {
            'listing': employe,
        }
        return render(request, 'sinistre/ajouter_sinistre.html', context)


def show_sinistre(request, pk):
    employe = Employe.objects.get(id=pk)

    sinistre = Sinistre.objects.filter(employe_id=employe.pk, soft_deleting=False)
    # peut-être une verification pour rediriger l'utilisateur sur la page de liste des employés au cas ou celui ci n'a pas de sinistre

    # typsinistre = typesinistre(sinistre)
    context = {
        'listing': employe,
        'showsinistres': sinistre,
    }
    return render(request, 'sinistre/list_sinistre.html', context)


def edit_sinistre(request, pk):
    try:
        sinistre = Sinistre.objects.get(id=pk)
        employe = Employe.objects.get(id=sinistre.employe_id)

    except sinistre.DoesNotExist:
        messages.success(request, "sinistre n'existe pas")

    if request.method == 'POST':

        if not request.POST['sinistreype'] and not request.POST['debutsinistre']:

            messages.error(request, "Mise à jour de sinistre Échouée", "danger")
        else:

            typesinistre = request.POST['sinistreype']
            datedebut = request.POST['debutsinistre']
            datefin = request.POST['finsinistre']
            salairemp = request.POST['paye']
            missionemp = request.POST['role']

            # Calcul de la durée de sinistre

            sinistre.typesinistre = typesinistre
            sinistre.mission = missionemp

            sinistre.datedebut = datedebut
            sinistre.datefin = datefin
            sinistre.salaire = salairemp
            sinistre.employe_id = employe.pk

            sinistre.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        messages.success(request, "Modification Effectuée", "success")
        return redirect('liste_employe')
    else:
        context = {
            'listing': employe,
            'showsinistres': sinistre,
        }
        return render(request, 'sinistre/edit_sinistre.html', context)



def del_sinistre(request, pk):
        try:
            sinistre = Sinistre.objects.get(id=pk)

        except sinistre.DoesNotExist:
            messages.success(request, "sinistre n'existe pas")

        sinistre.soft_deleting = True
        sinistre.save()
        messages.success(request, "sinistre Supprimé")
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
