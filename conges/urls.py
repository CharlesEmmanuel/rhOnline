
from django.urls import path, include
from conges.views import liste_empl, add_conges, show_conges, edit_conges, del_conges, ajout_tconges, delete_tconges, \
    edit_tconges, submit_conges
from mysite import settings

urlpatterns = [
    # Congés links
    path('liste/emp', liste_empl, name='conges_liste_emp'),
    path('add/<int:pk>', add_conges, name='conges_ajout'), # Ajout de conges à un employé
    path('list/<int:pk>', show_conges, name='conges_show'), # Liste des conges d'un employé

    path('submit/<int:pk>', submit_conges, name='soumettre_conges'), # Soumettre demande de congés

    path('edit/<int:pk>', edit_conges, name='conges_edit'), # Modification conges d'un employé
    path('delete/<int:pk>', del_conges, name='conges_del'), # Suppression conges d'un employé

    # Type Congés links
    path('typeconges/add', ajout_tconges, name='add_tconges'),
    path('typeconges/delete/<int:pk>', delete_tconges, name='delete_tconges'),
    path('typeconges/edit/<int:pk>', edit_tconges, name='edit_tconges'),

]
