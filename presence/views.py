from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import datetime
from employe.models import Employe
from presence.models import Pointage,Presence
from employe.backEnd import FaceRecognition
from django.contrib import messages
from employe.permissions import show_permission, access_permission

facerecognition = FaceRecognition()
def update_attendance_in_db_in(face_id):
    today = datetime.date.today()
    time = datetime.datetime.now()

    employee=Employe.objects.get(faceid=face_id)
    print(employee.name)
    try:
        requette = Presence.objects.get(employe=employee, date=today)
    except:
        requette = None
    if requette is None:
        if employee.faceid == face_id:

            pointage = Pointage(employee=employee, date=today,date_time=time, present=True,is_out=False)
            pointage.save()
            presence = Presence(employe=employee, datedebut=time)
            presence.save()

        else:
            # Message à retourné
            print("Vous n'est pas reconnu")

    else:
        if employee.faceid == face_id:

            # Message : Bienvenue
            print("Message : Bienvenue")
            requette.state = True
            requette.save()
    return requette

def update_attendance_in_db_out(face_id):
    today = datetime.date.today()
    time = datetime.datetime.now()
    employee = Employe.objects.get(faceid=face_id)
    print(employee.name)
    try:
        requette = Presence.objects.get(employe=employee, date=today)
    except:
        requette = None
    if employee.faceid == face_id:
        if requette is None:
            # Message :
            pointage = Pointage(employee=employee, date=today, date_time=time, present=True, is_out=True)
            pointage.save()

            presence = Presence(employe=employee, datefin=time)
            presence.save()

        else:
            pointage = Pointage(employee=employee, date=today, date_time=time, present=True, is_out=True)
            pointage.save()

            requette.datefin = time
            requette.save()

    return requette

def checkin_face(request):
    face_id = facerecognition.recognizeFace()
    print(face_id)
    print(face_id)
    employe_scanned = Employe.objects.get(faceid=face_id)

    timer = update_attendance_in_db_in(face_id)
    print(timer.update_at)
    context = {
        'tags': 'entree',
        'employe': employe_scanned,
        'typetag': "d'arrivée",
        'timer': timer
    }
    return render(request, 'presence/user_scanned_new.html', context)

def checkout_face(request):
    face_id = facerecognition.recognizeFace()
    print(face_id)
    # users = Employe.objects.get(faceid=face_id)
    timer = update_attendance_in_db_out(face_id)
    print(timer.update_at)
    employe_scanned = Employe.objects.get(faceid=face_id)
    context = {
        'tags': 'sortie',
        'employe': employe_scanned,
        'typetag': "de départ",
        'timer': timer
    }
    return render(request, 'presence/user_scanned_new.html', context)

@login_required(login_url="login")
def liste_presence(request):
    if access_permission(request):
        presence_liste = Presence.objects.all()
    else:
        pk = request.user.id
        try:
            employe = Employe.objects.get(account=pk)
            presence_liste = Presence.objects.filter(employe=employe).order_by('-id')

        except employe.DoesNotExist:
            messages.success(request, "Employé n'existe pas")

    context = {
        'listing': presence_liste
    }
    return render(request, 'presence/liste_presence.html', context)