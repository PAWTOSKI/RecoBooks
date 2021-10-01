

print("\t \tBienvenue de systeme de recommendation")
print("%30s" %("Recobook".upper()))
print("Groupe: Souad - Wilried - Nga")
print("\n")
ansUser = input("Vous êtes nouveau utilisateur (Yes-Oui/No-Non) : ")
if (str(ansUser).lower() == "oui") | (str(ansUser).lower() == "yes") | (str(ansUser).lower() == "o"):
        print("Quel genre de livre préférez-vous ?")
else:
    identity = input("Votre identifiant: ")
    try:
        identity = int(identity)
    except ValueError:
        print("Désolé la valeur saisie n'est pas un nombre.")
    

