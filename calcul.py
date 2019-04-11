def calcul(valeur, poids):
     """
          prix_total = valeur + douane + frais
     """
    if(poids != 0 and valeur < 66000):
         douane = 20000
         frais = poids * 6500
         prix_total = valeur + frais + 
print(calcul(10000, 0))