import datetime


def typecontrat(contrats):


        if contr.typecontrat == 'STG':
            contrat = 'Stage'
        elif contr.typecontrat == 'CDD':
            contrat = 'Contrat à durée déterminé'
        else:
            contrat = 'Contrat à durée indéterminé'
        return dict(contrat=contrat)
