from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib import messages
from datetime import datetime

from django.urls import reverse

from employe.models import Employe
from contrat.models import Contrat
from django.contrib.auth.decorators import login_required

from employe.permissions import show_permission, access_permission


@login_required(login_url="login")
def liste_empl(request):
    if access_permission(request):
        employe_list = Employe.objects.filter(soft_deleting=False)
        context = {
            'listing': employe_list
        }
        return render(request, 'contrat/liste_emp.html', context)
    else:
        return render(request, 'error_pages/errors-404.html')


@login_required(login_url="login")
def add_contrat(request, pk):
    if access_permission(request):
        try:
            employe = Employe.objects.get(id=pk)

        except employe.DoesNotExist:
            messages.success(request, "Employé n'existe pas")

        if request.method == 'POST':

            if not request.POST['contratype'] and not request.POST['debutcontrat']:

                messages.error(request, "Ajout de Contrat Échouée", "danger")
            else:

                typecontrat = request.POST['contratype']
                datedebut = request.POST['debutcontrat']
                datefin = request.POST['fincontrat']
                salairemp = request.POST['paye']
                missionemp = request.POST['role']

                # Calcul de la durée de contrat

                contrat = Contrat()

                contrat.typecontrat = typecontrat
                contrat.mission = missionemp

                contrat.datedebut = datedebut
                contrat.datefin = datefin
                contrat.salaire = salairemp
                contrat.employe_id = employe.pk

                contrat.save()

                # Code d'ajout du contrat

                messages.success(request, "Contrat Enrégistré", "success")
                return redirect('contrat_liste_emp')
        else:
            context = {
                'listing': employe,
            }
            return render(request, 'contrat/ajouter_contrat.html', context)
    else:
        return render(request, 'error_pages/errors-404.html')


@login_required(login_url="login")
def show_contrat(request, pk):
    if show_permission(request, pk):
        employe = Employe.objects.get(id=pk)

        contrat = Contrat.objects.filter(employe_id=employe.pk, soft_deleting=False)
        # peut-être une verification pour rediriger l'utilisateur sur la page de liste des employés au cas ou celui ci n'a pas de contrat

        context = {
            'listing': employe,
            'showcontrats': contrat,
        }
        return render(request, 'contrat/list_contrat.html', context)

    else:
        return render(request, 'error_pages/errors-404.html')


@login_required(login_url="login")
def edit_contrat(request, pk):
    if access_permission(request):
        try:
            contrat = Contrat.objects.get(id=pk)
            employe = Employe.objects.get(id=contrat.employe_id)

        except contrat.DoesNotExist:
            messages.success(request, "Contrat n'existe pas")

        if request.method == 'POST':

            if not request.POST['contratype'] and not request.POST['debutcontrat']:

                messages.error(request, "Mise à jour de Contrat Échouée", "danger")
            else:

                typecontrat = request.POST['contratype']
                datedebut = request.POST['debutcontrat']
                datefin = request.POST['fincontrat']
                salairemp = request.POST['paye']
                missionemp = request.POST['role']

                # Calcul de la durée de contrat

                contrat.typecontrat = typecontrat
                contrat.mission = missionemp

                contrat.datedebut = datedebut
                contrat.datefin = datefin
                contrat.salaire = salairemp
                contrat.employe_id = employe.pk

                contrat.save()

                idemp = employe.pk

                messages.success(request, "Modification Effectuée", "success")
                return redirect(reverse('contrat_show',args=[idemp]))

        else:
            context = {
                'listing': employe,
                'showcontrats': contrat,
            }
            return render(request, 'contrat/edit_contrat.html', context)
    else:
        return render(request, 'error_pages/errors-404.html')





@login_required(login_url="login")
def del_contrat(request, pk):
    if access_permission(request):
        try:
            contrat = Contrat.objects.get(id=pk)
            employe = Employe.objects.get(id=contrat.employe_id)

        except contrat.DoesNotExist:
            messages.success(request, "Contrat n'existe pas")

        contrat.soft_deleting = True
        contrat.save()

        messages.success(request, "Contrat Supprimé")

        idemp = employe.pk

        return redirect(reverse('contrat_show', args=[idemp]))
    else:
        return render(request, 'error_pages/errors-404.html')