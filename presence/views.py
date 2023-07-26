from django.shortcuts import render, redirect
import datetime
import math
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from matplotlib import rcParams
# Create your views here.
from employe.models import Employe
from presence.models import Pointage
from django_pandas.io import read_frame
from presence.models import Pointage,Presence
from pandas.plotting import register_matplotlib_converters
import seaborn as sns
from django.contrib import messages

from employe.backEnd import FaceRecognition

facerecognition = FaceRecognition()
def update_attendance_in_db_in(face_id):
    today = datetime.date.today()
    time = datetime.datetime.now()

    employee=Employe.objects.get(faceid=face_id)
    print(employee.name)
    try:
        requette = Pointage.objects.get(employee=employee, date=today)
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
            # requette.present = True
            # requette.save(update_fields=['present'])

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


def checkin_face(request):
    face_id = facerecognition.recognizeFace()
    employe = Employe.objects.get(faceid=face_id)

    update_attendance_in_db_in(face_id)

    context = {
        'listing': employe
    }
    return render(request, 'presence/user_scanned_new.html', context)

def checkout_face(request):
    face_id = facerecognition.recognizeFace()
    print(face_id)
    users = Employe.objects.get(faceid=face_id)
    update_attendance_in_db_out(face_id)

    employe_list = Employe.objects.filter(soft_deleting=False)
    context = {
        'listing': employe_list
    }
    return render(request, 'presence/user_scanned.html', context)


def liste_presence(request):
    presence_liste = Presence.objects.all()
    context = {
        'listing': presence_liste
    }
    return render(request, 'presence/liste_presence.html', context)