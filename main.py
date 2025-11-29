import sys
import glob
import os

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
        if os.path.isfile(f"{dossierAScanner}/{fichier}"):
            extension = fichier.split('.')
            extension = extension[len(extension) - 1]

            # On comptabilise l'extension trouvée
            if extension in listeExtension:
                nombreOccurence = listeExtension[extension]
                nombreOccurence = nombreOccurence + 1
                listeExtension[extension] = nombreOccurence
            
            else:
                listeExtension[extension] = 1
    
    return listeExtension

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
        
    chemin_dossier = sys.argv[1]
    if not os.path.isdir(chemin_dossier):
        print(f"Erreur: le chemin fourni '{chemin_dossier}' n'est pas un dossier valide.")
        sys.exit(1)
    
    listeExtension = compter_type_fichier(chemin_dossier)

    # On vérifie qu'il n'y ait qu'un seul type de fichier image dans le dossier
    type_fichier_trouve = listeExtension.keys()
    type_image_trouve = EXTENSIONS_IMAGE.intersection(type_fichier_trouve)

    if len(type_image_trouve) > 1:
        print("Des fichiers images de différents type ont été trouvés, veuillez ne laisser qu'un seul type de fichier à traiter.")
        sys.exit(1)