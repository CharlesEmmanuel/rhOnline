from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from employe.views import liste_departement, delete_departement, liste_poste, delete_poste, edit_poste, liste_liemploi, \
    edit_liemploi, delete_liemploi, liste_emp, EmployeCreateView, delete_employe, edit_employe, addFace, scanFace
from mysite import settings

urlpatterns = [
    # Departements links
    path('departement/liste', liste_departement, name='liste_departement'),
    path('departement/delete/<int:pk>', delete_departement, name='delete_departement'),
    path('departement/edit/<int:pk>', edit_poste, name='edit_departement'),

    # Poste links
    path('poste/liste', liste_poste, name='liste_poste'),
    path('poste/delete/<int:pk>', delete_poste, name='delete_poste'),
    path('poste/edit/<int:pk>', edit_poste, name='edit_poste'),

    # Lieu Emploi links
    path('liemploi/liste', liste_liemploi, name='liste_liemploi'),
    path('liemploi/delete/<int:pk>', delete_liemploi, name='delete_liemploi'),
    path('liemploi/edit/<int:pk>', edit_liemploi, name='edit_liemploi'),



    # Employes

    path('create', EmployeCreateView.as_view(), name='create_employe'),

    path('scan/<int:face_id>', scanFace, name='scan_employe'),

    path('liste', liste_emp, name='liste_employe'),
    path('delete/<int:pk>', delete_employe, name='delete_employe'),
    path('edit/<int:pk>', edit_employe, name='edit_employe'),


]
