import sys
import glob
import os

# Fonction de vérification des dépendances
def check_dependencies():
    
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

# Exécution du script
if __name__ == "__main__":
    # Vérification des dépendances
    if not check_dependencies():
        print("Arrêt du script : les dépendances manquent.")
        sys.exit(1)