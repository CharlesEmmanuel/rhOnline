
from django.urls import path, include
from sinistre.views import liste_empl, add_sinistre, show_sinistre, edit_sinistre, del_sinistre
from mysite import settings

urlpatterns = [
    # Departements links
    path('liste/emp', liste_empl, name='sinistre_liste_emp'),
    path('add/<int:pk>', add_sinistre, name='sinistre_ajout'), # Ajout de sinistre à un employé
    path('list/<int:pk>', show_sinistre, name='sinistre_show'), # Liste des sinistres d'un employé

    path('edit/<int:pk>', edit_sinistre, name='sinistre_edit'), # Modification sinistre d'un employé
    path('delete/<int:pk>', del_sinistre, name='sinistre_del'), # Suppression sinistre d'un employé

]
