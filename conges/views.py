from django.shortcuts import render, redirect

from django.contrib import messages
from django.urls import reverse

from conges.forms import TypecongesForm
from conges.models import Conges, Typeconges
from employe.models import Employe
from django.contrib.auth.decorators import login_required
from employe.permissions import employe_permission, show_permission



# Class Parametres des type de congés

@login_required(login_url="login")
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

@login_required(login_url="login")
def delete_tconges(request, pk):
    global typeconges
    try:
        typeconges = Typeconges.objects.get(id=pk)

    except typeconges.DoesNotExist:
        messages.success(request, "Type congé n'existe pas")

    typeconges.delete()
    messages.success(request, "Type de congé Supprimé")
    return redirect('add_tconges')


@login_required(login_url="login")
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

@login_required(login_url="login")
def liste_empl(request):
    employe_list = Employe.objects.filter(soft_deleting=False)

    context = {
        'listing': employe_list,
    }
    return render(request, 'conges/liste_emp.html', context)


@login_required(login_url="login")
def add_conges(request, pk):
    if show_permission(request, pk):
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
                conges.description = description
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
    else:
        return render(request, 'error_pages/errors-404.html')


@login_required(login_url="login")
def show_conges(request, pk):
    if show_permission(request, pk):
        employe = Employe.objects.get(id=pk)

        conges = Conges.objects.filter(employe_id=employe.pk, soft_deleting=False)
        # peut-être une verification pour rediriger l'utilisateur sur la page de liste des employés au cas ou celui ci n'a pas de conges

        # typconges = typeconges(conges)
        context = {
            'listing': employe,
            'showconges': conges,
        }
        return render(request, 'conges/list_conges.html', context)
    else:
        return render(request, 'error_pages/errors-404.html')



@login_required(login_url="login")
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



@login_required(login_url="login")
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


            conges.typeconges_id = typecong
            conges.description = description

            conges.datedebut = datedebut
            conges.datefin = datefin
            conges.employe_id = employe.pk

            conges.save()

            idemp = employe.pk

            messages.success(request, "Modification Effectuée", "success")
            return redirect(reverse('conges_show', args=[idemp]))

    else:
        context = {
            'typeconges': Typeconges.objects.all(),
            'listing': employe,
            'showconges': conges,
        }
        return render(request, 'conges/edit_conges.html', context)


def valider_conges(request, pk):
    try:
        conges = Conges.objects.get(id=pk)

    except conges.DoesNotExist:
        messages.success(request, "conges n'existe pas")

    conges.etatconges = 'VAL'
    conges.save()
    messages.success(request, "Congé Accordé")

    employe = Employe.objects.get(id=conges.employe_id)
    idemp = employe.pk
    return redirect(reverse('conges_show', args=[idemp]))

def undo_conges(request, pk):
    try:
        conges = Conges.objects.get(id=pk)

    except conges.DoesNotExist:
        messages.success(request, "conges n'existe pas")

    conges.etatconges = 'REJ'
    conges.save()
    messages.error(request, "Demande Rejeté", "danger")

    employe = Employe.objects.get(id=conges.employe_id)
    idemp = employe.pk
    return redirect(reverse('conges_show', args=[idemp]))


@login_required(login_url="login")
def del_conges(request, pk):
        try:
            conges = Conges.objects.get(id=pk)

        except conges.DoesNotExist:
            messages.success(request, "conges n'existe pas")

        conges.soft_deleting = True
        conges.save()
        messages.error(request, "conges Supprimé", "danger")

        employe = Employe.objects.get(id=conges.employe_id)
        idemp = employe.pk
        return redirect(reverse('conges_show', args=[idemp]))
