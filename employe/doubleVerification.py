from conges.models import *
from contrat.models import *
from employe.models import *
from presence.models import *
from sinistre.models import *

def verificationDouble(Model,attr1,valeur):

    req2 = Model.objects.filter(attr1=valeur)
    print(str(req2))

    if req2:
       return True
    else:
        return False