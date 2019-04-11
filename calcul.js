function calcul(valeur, poids) {
     if (poids != 0 || valeur != 0) {
          if (valeur < 66000) {
               var douane = 20000;
          } else {
               var douane = valeur / 2;
          }
          var frais = poids * 6500;
          var total = valeur + douane + frais;
          console.log("Les frais de douane sont: "+ frais)
          console.log("Les frais de livraison selon le poids sont: " + frais)
          console.log("Le total à payer est de: " + total)
     } else {
          console.log("Données invalides")
     }
     
     return total
}

calcul(30000, 1)