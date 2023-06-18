from django.shortcuts import render, redirect
from django.views.generic import CreateView

from employe.forms import DepartementForm, PosteForm, LiemploiForm, EmployeForm
from django.contrib import messages
from datetime import datetime
from employe.models import Departement, Poste, LieuEmploi, Employe, Account

from employe.backEnd import FaceRecognition
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

facerecognition = FaceRecognition()

# Create your views here.

@login_required(login_url="login")
def liste_departement(request):
    # print(request.name) A FAIRE UNE VERIFICATION DES INFORMATIONS ENTREES PAS L'UTILISATEUR ( CHAMPS VIDES )
    # breakpoint()
    if request.method == 'POST':
        forms = DepartementForm(request.POST)
        if forms.is_valid():
            if not forms.data['name'] and not forms.data['description']:
                messages.error(request, "Departement non enregistré", "danger")
            else:
                forms.save()
                messages.success(request, "Departement enregistré", "success")
        else:
            messages.error(request, "Departement non enregistré", "danger")

    form_dep = DepartementForm
    departement_list = Departement.objects.filter(soft_deleting=False)
    context = {
        'forms': form_dep,
        'listing': departement_list,
    }

    return render(request, 'departement/liste_departement.html', context)


@login_required(login_url="login")
def delete_departement(request, pk):
    try:
        departement = Departement.objects.get(id=pk)

    except Departement.DoesNotExist:
        messages.error(request, "Departement n'existe pas", "danger")

    departement.soft_deleting = True
    departement.save()
    messages.error(request, "Departement Supprimé", "danger")
    return redirect('liste_departement')


@login_required(login_url="login")
def edit_departement(request, pk):
    departement = Departement.objects.get(id=pk)
    if request.method == 'POST':
        forms = DepartementForm(request.POST, instance=departement)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Departement enregistré", "success")
            return redirect('liste_departement')
        else:
            messages.error(request, "Departement non enregistré", "danger")
            return redirect('liste_departement')
    else:
        form_dep = DepartementForm(instance=departement)

        departement_list = Departement.objects.filter(soft_deleting=False)
        context = {
            'forms': form_dep,
            'listing': departement_list,

        }
        return render(request, 'departement/liste_departement.html', context)


@login_required(login_url="login")
def liste_poste(request):
    if request.method == 'POST':
        forms = PosteForm(request.POST)
        if forms.is_valid():
            if not forms.data['name'] and not forms.data['description']:
                messages.error(request, "Poste non enregistré", "danger")
            else:
                forms.save()
                messages.success(request, "Poste enregistré", "success")
        else:
            messages.success(request, "Poste non enregistré")

    form_post = PosteForm
    poste_list = Poste.objects.filter(soft_deleting=False)
    context = {
        'forms': form_post,
        'listing': poste_list
    }

    return render(request, 'poste/liste_poste.html', context)


@login_required(login_url="login")
def delete_poste(request, pk):
    try:
        poste = Poste.objects.get(id=pk)

    except Poste.DoesNotExist:
        messages.success(request, "Poste n'existe pas")

    poste.soft_deleting = True
    poste.save()
    messages.success(request, "Poste Supprimé")
    return redirect('liste_poste')


@login_required(login_url="login")
def edit_poste(request, pk):
    poste = Poste.objects.get(id=pk)
    if request.method == 'POST':
        forms = PosteForm(request.POST, instance=poste)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Poste enregistré", "success")
            return redirect('liste_poste')
        else:
            messages.error(request, "Poste non enregistré", "danger")
            return redirect('liste_poste')
    else:
        form_poste = PosteForm(instance=poste)

        poste_list = Poste.objects.filter(soft_deleting=False)
        context = {
            'forms': form_poste,
            'listing': poste_list,

        }
        return render(request, 'poste/liste_poste.html', context)


@login_required(login_url="login")
def liste_liemploi(request):
    if request.method == 'POST':
        forms = LiemploiForm(request.POST)
        if forms.is_valid():
            if not forms.data['name'] and not forms.data['description']:
                messages.error(request, "Lieu non enregistré", "danger")
            else:
                forms.save()
                messages.success(request, "Lieu enregistré", "success")
        else:
            messages.success(request, "lieu non enregistré")

    form_liemploi = LiemploiForm
    liemploi_list = LieuEmploi.objects.filter(soft_deleting=False)
    context = {
        'forms': form_liemploi,
        'listing': liemploi_list
    }

    return render(request, 'lieuemploi/liste_lieuemploi.html', context)


@login_required(login_url="login")
def delete_liemploi(request, pk):
    try:
        liemploi = LieuEmploi.objects.get(id=pk)

    except liemploi.DoesNotExist:
        messages.success(request, "Poste n'existe pas")

    liemploi.soft_deleting = True
    liemploi.save()
    messages.success(request, "Lieu Supprimé")
    return redirect('liste_liemploi')


@login_required(login_url="login")
def edit_liemploi(request, pk):
    liemploi = LieuEmploi.objects.get(id=pk)
    if request.method == 'POST':
        forms = LiemploiForm(request.POST, instance=liemploi)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Lieu enregistré", "success")
            return redirect('liste_liemploi')
        else:
            messages.error(request, "Lieu non enregistré", "danger")
            return redirect('liste_liemploi')
    else:
        form_liemploi = LiemploiForm(instance=liemploi)

        liemploi_list = LieuEmploi.objects.filter(soft_deleting=False)
        context = {
            'forms': form_liemploi,
            'listing': liemploi_list,
        }
        return render(request, 'lieuemploi/liste_lieuemploi.html', context)




@method_decorator(login_required(login_url="login"), name='get')
class EmployeCreateView(CreateView):
    list_em = Employe.objects.filter(soft_deleting=False)
    template_name = 'employe/ajouter_employe.html'

    context = {
        'departements': Departement.objects.all(),
        'lieuemp': LieuEmploi.objects.all(),
        'postes': Poste.objects.all(),
    }


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


    def post(self, request, *args, **kwargs):
        self.object = None
        if request.POST:
            self.form_valid_emp(request)
            messages.success(request, "Employé enregistré avec succès", "success")
            return redirect('create_employe')
        else:
            pass

    def form_valid_emp(self, request):
        if not request.POST['frist_name'] and not request.POST['last_name'] and not request.POST['mail'] and not \
                request.POST['dapartmpnt'] and not request.POST['unposted'] and not request.POST['telephone']:
            messages.error(request, "Employé non enregistré", "danger")
        else:

            nom = request.POST['frist_name']
            prenom = request.POST['last_name']
            email = request.POST['mail']
            passwd = request.POST['motdepass']
            user_type = request.POST['type_cmp']

            departement = request.POST['dapartmpnt']
            liemploi = request.POST['lieuservice']
            poste = request.POST['unposted']
            adresse = request.POST['localite']
            genre = request.POST['genrehumain']
            datenaiss = request.POST['naissance']

            tel1 = request.POST['telephone']
            tel2 = request.POST['cellulaire']
            numbanq = request.POST['bancaire']
            statutmat = request.POST['situation']
            nbreenf = request.POST['enfants']
            numurgence = request.POST['casurgence']


            employe = Employe()

            account = Account.objects.create_user(nom,prenom,email,user_type=user_type,password=passwd)

            employe.faceid = account.pk

            employe.name = nom
            employe.prenom = prenom
            employe.emailemp = email
            employe.account_id = account.pk
            employe.departement_id = departement
            employe.lieuemploie_id = liemploi
            employe.poste_id = poste
            employe.adress = adresse
            employe.genre = genre
            employe.datenaiss = datenaiss
            employe.phone1 = tel1
            employe.phone2 = tel2
            employe.numbank = numbanq
            employe.statutmat = statutmat
            employe.nbrechild = nbreenf
            employe.contacturgence = numurgence
            employe.save()

            addFace(employe.faceid)

# Fonction listing des employes
@login_required(login_url="login")
def liste_emp(request):
    employe_list = Employe.objects.filter(soft_deleting=False)
    context = {
        'listing': employe_list
    }
    return render(request, 'employe/liste_employe.html', context)


# Fonction Suppression d'employé
@login_required(login_url="login")
def delete_employe(request, pk):
    try:
        employe = Employe.objects.get(id=pk)
        account = Account.objects.get(id=employe.account_id)

    except employe.DoesNotExist:
        messages.success(request, "Employé n'existe pas")

    account.soft_deleting = True
    employe.soft_deleting = True
    account.save()
    employe.save()
    messages.success(request, "Employé Supprimé")
    return redirect('liste_employe')

@login_required(login_url="login")
def edit_employe(request, pk):
    try:
        employe = Employe.objects.get(id=pk)
        account = Account.objects.get(id=employe.account_id)

    except employe.DoesNotExist:
        messages.success(request, "Employé n'existe pas")

    if request.method == 'POST':

        if not request.POST['frist_name'] and not request.POST['last_name'] and not request.POST['mail'] and not \
                request.POST['dapartmpnt'] and not request.POST['unposted'] and not request.POST['telephone']:
            messages.error(request, "Modification Échouée", "danger")
        else:

            nom = request.POST['frist_name']
            prenom = request.POST['last_name']
            email = request.POST['mail']
            user_type = request.POST['type_cmp']

            departement = request.POST['dapartmpnt']
            liemploi = request.POST['lieuservice']
            poste = request.POST['unposted']
            adresse = request.POST['localite']
            genre = request.POST['genrehumain']
            datenaiss = request.POST['naissance']

            tel1 = request.POST['telephone']
            tel2 = request.POST['cellulaire']
            numbanq = request.POST['bancaire']
            statutmat = request.POST['situation']
            nbreenf = request.POST['enfants']
            numurgence = request.POST['casurgence']

            account.first_name = nom
            account.last_name = prenom
            account.email = email
            account.user_type = user_type
            account.save()

            employe.faceid = account.pk

            employe.name = nom
            employe.prenom = prenom
            employe.emailemp = email
            employe.account_id = account.pk
            employe.departement_id = departement
            employe.lieuemploie_id = liemploi
            employe.poste_id = poste
            employe.adress = adresse
            employe.genre = genre
            employe.datenaiss = datenaiss
            employe.phone1 = tel1
            employe.phone2 = tel2
            employe.numbank = numbanq
            employe.statutmat = statutmat
            employe.nbrechild = nbreenf
            employe.contacturgence = numurgence
            employe.save()

        messages.success(request, "Modification Effectuée", "success")
        return redirect('liste_employe')
    else:
        context = {
            'listing': employe,
            'compte': account,
            'departements': Departement.objects.filter(soft_deleting=False),
            'lieuemp': LieuEmploi.objects.filter(soft_deleting=False),
            'postes': Poste.objects.filter(soft_deleting=False),
        }
        return render(request, 'employe/edit_employe.html', context)




@login_required(login_url="login")
def addFace(face_id):
    face_id = face_id
    facerecognition.faceDetect(face_id)
    facerecognition.trainFace()
    return redirect('/')


@login_required(login_url="login")
def scanFace(request,face_id):
    face_id = face_id
    facerecognition.faceDetect(face_id)
    facerecognition.trainFace()
    return redirect('/')



@login_required(login_url="login")
def fiche_employe(request, pk):

    employe = Employe.objects.get(id=pk)
    account = Account.objects.get(id=employe.account_id)

    context = {
        'listing': employe,
        'compte': account,
        'departements': Departement.objects.filter(soft_deleting=False),
        'lieuemp': LieuEmploi.objects.filter(soft_deleting=False),
        'postes': Poste.objects.filter(soft_deleting=False),
    }

    return render(request, 'employe/fiche_employe.html', context)
