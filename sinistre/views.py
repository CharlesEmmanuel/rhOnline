from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib import messages
from django.urls import reverse

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

        if not request.POST['explain'] and not request.POST['datedeclaration']:

            messages.error(request, "Ajout de sinistre Échouée", "danger")
        else:

            dateevent = request.POST['datedeclaration']
            description = request.POST['explain']

            # Calcul de la durée de sinistre

            sinistre = Sinistre()

            sinistre.description = description

            sinistre.datesinistre = dateevent
            sinistre.employe_id = employe.pk

            sinistre.save()

            # Code d'ajout du sinistre
            idemp = employe.pk
            messages.success(request, "sinistre Enrégistré", "success")

            return redirect(reverse('sinistre_show', args=[idemp]))

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

        if not request.POST['datedeclaration'] and not request.POST['explain']:

            messages.error(request, "Mise à jour de sinistre Échouée", "danger")
        else:


            dateevent = request.POST['datedeclaration']
            description = request.POST['explain']

            # Calcul de la durée de sinistre

            sinistre.description = description

            sinistre.datesinistre = dateevent
            sinistre.employe_id = employe.pk

            sinistre.save()

            idemp = employe.pk
            messages.success(request, "sinistre modifié", "success")
            return redirect(reverse('sinistre_show', args=[idemp]))

    else:
        context = {
            'listing': employe,
            'showsinistre': sinistre,
        }
        return render(request, 'sinistre/edit_sinistre.html', context)


def del_sinistre(request, pk):
    try:
        sinistre = Sinistre.objects.get(id=pk)

    except sinistre.DoesNotExist:
        messages.success(request, "sinistre n'existe pas")

    sinistre.soft_deleting = True
    sinistre.save()

    idemp = sinistre.employe_id
    messages.success(request, "sinistre supprimé", "danger")
    return redirect(reverse('sinistre_show', args=[idemp]))
