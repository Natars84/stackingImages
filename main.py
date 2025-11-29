import sys
import glob
import os

# Les extensions d'images prises en charge
EXTENSIONS_IMAGE = {
    'jpg', 'jpeg', 'png', 'gif',
    'bmp', 'svg', 'webp', 'tif',
    'tiff', 'dng', 'ico', 'hdr'
}

# Fonction de vérification des dépendances
def verifier_dependences():
    
    # Vérification 1: Wand (Python)
    try:
        from wand.version import VERSION
    except:
        print("❌ Erreur: La librairie Python 'Wand' n'est pas installée ('pip install Wand').")
        return False
    
    # Vérification 2: Liaison avec ImageMagick (librairie C)
    try:
        from wand.api import library
        library.MagickGetCopyright()
        return True
        
    except Exception as e:
        print("❌ Erreur: Wand n'a pas pu se lier à la librairie ImageMagick.")
        print(f"   Détails: {e}")
        print("\n   ACTION REQUISE: Installez ou réinstallez ImageMagick sur votre système.")
        return False

# Fonction qui liste et comptabilise le nombre de fichier par extension trouvée dans le dossier donné
def compter_type_fichier(dossierAScanner: str):
    listeExtension = {}
    liste_fichiers = os.listdir(dossierAScanner)

    # Pour chacun des fichiers, on extrait l'extension
    for fichier in liste_fichiers:
        fichier = os.path.join(dossierAScanner, fichier)

        if os.path.isfile(f"{dossierAScanner}/{fichier}"):
            extension = os.path.splitext(fichier)[1].lstrip('.').lower()

            # On comptabilise l'extension trouvée
            listeExtension[extension] = listeExtension.get(extension, 0) + 1
    
    return listeExtension

# Fonction chargée de demander une information à l'utilisateur. Elle peut contraindre sa réponse à une liste définie.
# Elle renvoie sa réponse en tant que string
def demander_information_string(question: str, reponses_possibles: set = None) -> str:
    if reponses_possibles is None:
        reponses_possibles = set() # Utilise un set vide si aucun n'est fourni

    reponse_utilisateur = ""
    
    reponses_possibles_upper = {r.upper().strip() for r in reponses_possibles}

    if len(reponses_possibles_upper) >= 1:
        while reponse_utilisateur not in reponses_possibles_upper:
            reponse_utilisateur = input(question + " (Rép. possibles : " + ", ".join(reponses_possibles) + ") ").upper().strip()
            
            if not reponse_utilisateur and len(reponses_possibles_upper) > 0:
                continue

    else:
        reponse_utilisateur = input(question).upper().strip()
    
    return reponse_utilisateur

# Exécution du script
if __name__ == "__main__":

    # Vérification des dépendances
    if not verifier_dependences():
        print("Arrêt du script : les dépendances manquent.")
        sys.exit(1)

    # Analyse du contenu du dossier fourni en argument
    if len(sys.argv) < 2:
        print("Erreur: veuillez fournir le chemin du dossier contenant les images.")
        sys.exit(1)

    if not os.path.isdir(sys.argv[1]):
        print(f"Erreur: le chemin fourni '{sys.argv[1]}' n'est pas un dossier valide.")
        sys.exit(1)
    
    # Le dossier contenant les photos à traiter
    DOSSIER_PHOTO = os.path.abspath(sys.argv[1])

    listeExtension = compter_type_fichier(DOSSIER_PHOTO)

    # On vérifie qu'il n'y ait qu'un seul type de fichier image dans le dossier
    type_fichier_trouve = listeExtension.keys()
    type_image_trouve = EXTENSIONS_IMAGE.intersection(type_fichier_trouve)

    if len(type_image_trouve) > 1:
        print("Des fichiers images de différents type ont été trouvés, veuillez ne laisser qu'un seul type de fichier à traiter.")
        sys.exit(1)
    
    #################################
    ##### TRAITEMENT DES PHOTOS #####
    #################################
    DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS = "tmp"

    if DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS in os.listdir(DOSSIER_PHOTO):
        question = "Un dossier temporaire contenant les photos en cours de traitement a été trouvé.\n" \
        "Si vous souhaitez poursuivre l'installation, ce dossier sera supprimé.\n" \
        "\nVoulez-vous continuer ?"

        reponse_accepte = ["O", "OUI", "N", "NON", "Y", "YES", "N", "NO"]
        reponse_utilisateur = demander_information_string(question, reponse_accepte)

        print(f"L'utilisateur a finalement répondu: {reponse_utilisateur}")