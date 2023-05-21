
from django.urls import path, include
from contrat.views import liste_empl, add_contrat, show_contrat, edit_contrat, del_contrat
from mysite import settings

urlpatterns = [
    # Departements links
    path('liste/emp', liste_empl, name='contrat_liste_emp'),
    path('add/<int:pk>', add_contrat, name='contrat_ajout'), # Ajout de Contrat à un employé
    path('list/<int:pk>', show_contrat, name='contrat_show'), # Liste des Contrats d'un employé

    path('edit/<int:pk>', edit_contrat, name='contrat_edit'), # Modification Contrat d'un employé
    path('delete/<int:pk>', del_contrat, name='contrat_del'), # Suppression Contrat d'un employé

]
