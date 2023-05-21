from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib import messages
from django.urls import reverse

from conges.forms import TypecongesForm
from conges.models import Conges, Typeconges
from employe.models import Employe


# Class Parametres des type de congés

def ajout_tconges(request):
    if request.method == 'POST':
        forms = TypecongesForm(request.POST)
        if forms.is_valid():
            if not forms.data['name'] and not forms.data['description']:
                messages.error(request, "Type de congé Non enregistré", "danger")
            else:
                forms.save()
                messages.success(request, "Type de congé enregistré", "success")
        else:
            messages.error(request, "ype de congé Non enregistré")

    form_typeconges = TypecongesForm
    typeconges_list = Typeconges.objects.all()
    context = {
        'forms': form_typeconges,
        'listing': typeconges_list
    }

    return render(request, 'typeconges/liste_typeconges.html', context)
#

def delete_tconges(request, pk):
    try:
        typeconges = Typeconges.objects.get(id=pk)

    except typeconges.DoesNotExist:
        messages.success(request, "Type congé n'existe pas")

    typeconges.delete()
    messages.success(request, "Type de congé Supprimé")
    return redirect('add_tconges')


def edit_tconges(request, pk):
    typeconges = Typeconges.objects.get(id=pk)
    if request.method == 'POST':
        forms = TypecongesForm(request.POST, instance=typeconges)

        if forms.is_valid():
            forms.save()
            messages.success(request, "Type de congé Modifié", "success")
            return redirect('add_tconges')
        else:
            messages.error(request, "Type de congé non enregistré", "danger")
            return redirect('add_tconges')
    else:
        form_typeconge = TypecongesForm(instance=typeconges)

        typeconges_list = Typeconges.objects.all()
        context = {
            'forms': form_typeconge,
            'listing': typeconges_list
        }

        return render(request, 'typeconges/liste_typeconges.html', context)



# Class d'ajout de congés

def liste_empl(request):
    employe_list = Employe.objects.filter(soft_deleting=False)

    context = {
        'listing': employe_list,
    }
    return render(request, 'conges/liste_emp.html', context)


def add_conges(request, pk):
    try:
        employe = Employe.objects.get(id=pk)
        typeconges_list = Typeconges.objects.all()

    except employe.DoesNotExist:
        messages.success(request, "Employé n'existe pas")

    if request.method == 'POST':

        if not request.POST['congesype'] and not request.POST['debutconges']:

            messages.error(request, "Ajout de conges Échouée", "danger")
        else:
            typecong = request.POST['congesype']
            datedebut = request.POST['debutconges']
            datefin = request.POST['finconges']
            description = request.POST['explain']

            state = 'NEW'

            # Calcul de la durée de conges

            conges = Conges()

            conges.typeconges_id = typecong
            conges.desciption = description
            conges.etatconges = state

            conges.datedebut = datedebut
            conges.datefin = datefin
            conges.employe_id = employe.pk

            conges.save()

            # Code d'ajout du conges
            idemp = employe.pk

            messages.success(request, "conges Enrégistré", "success")
            return redirect(reverse('conges_show',args=[idemp]))
    else:
        context = {
            'listing': employe,
            'typeconges': typeconges_list
        }
        return render(request, 'conges/ajouter_conges.html', context)


def show_conges(request, pk):
    employe = Employe.objects.get(id=pk)

    conges = Conges.objects.filter(employe_id=employe.pk, soft_deleting=False)
    # peut-être une verification pour rediriger l'utilisateur sur la page de liste des employés au cas ou celui ci n'a pas de conges

    # typconges = typeconges(conges)
    context = {
        'listing': employe,
        'showconges': conges,
    }
    return render(request, 'conges/list_conges.html', context)



def submit_conges(request, pk):
    try:
        conges = Conges.objects.get(id=pk)
        employe = Employe.objects.get(id=conges.employe_id)

    except conges.DoesNotExist:
        messages.success(request, "Employé n'existe pas")

    state = 'ATT'

    conges.etatconges = state
    conges.save()
    # Code d'ajout du conges
    idemp = employe.pk

    messages.success(request, "Demande Envoyée", "success")
    return redirect(reverse('conges_show',args=[idemp]))

























def edit_conges(request, pk):
    try:
        conges = Conges.objects.get(id=pk)
        employe = Employe.objects.get(id=conges.employe_id)

    except conges.DoesNotExist:
        messages.success(request, "conges n'existe pas")

    if request.method == 'POST':

        if not request.POST['congesype'] and not request.POST['debutconges']:

            messages.error(request, "Mise à jour de conges Échouée", "danger")
        else:

            typecong = request.POST['congesype']
            datedebut = request.POST['debutconges']
            datefin = request.POST['finconges']
            description = request.POST['explain']

            state = 'NEW'

            # Calcul de la durée de conges

            conges = Conges()

            conges.typeconges_id = typecong
            conges.desciption = description
            conges.etatconges = state

            conges.datedebut = datedebut
            conges.datefin = datefin
            conges.employe_id = employe.pk

            conges.save()

            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)

        messages.success(request, "Modification Effectuée", "success")
        return redirect('liste_employe')
    else:
        context = {
            'listing': employe,
            'showconges': conges,
        }
        return render(request, 'conges/edit_conges.html', context)


def del_conges(request, pk):
        try:
            conges = Conges.objects.get(id=pk)

        except conges.DoesNotExist:
            messages.success(request, "conges n'existe pas")

        conges.soft_deleting = True
        conges.save()
        messages.success(request, "conges Supprimé")
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
