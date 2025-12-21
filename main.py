import sys
import os
import time
import shutil
from typing import Tuple, List, Union, Set, Optional

# Quantite maximale de RAM que peut utiliser ImageMagick
TAILLE_MAX_RAM_GO_UTILISABLE = 4

# Quantite maximale d'espace disque que peut utiliser ImageMagick
TAILLE_MAX_DISQUE_DUR_GO_UTILISABLE = 8

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
		print("\n	ACTION REQUISE: Installez ou réinstallez ImageMagick sur votre système.")
		return False

# Fonction qui liste et comptabilise le nombre de fichier par extension trouvée dans le dossier donné
def compter_type_fichier(dossierAScanner: str):
	listeExtension = {}
	liste_fichiers = os.listdir(dossierAScanner)

	# Pour chacun des fichiers, on extrait l'extension
	for fichier in liste_fichiers:

		if os.path.isfile(f"{dossierAScanner}/{fichier}"):
			extension = os.path.splitext(fichier)[1].lstrip('.').lower()

			# On comptabilise l'extension trouvée
			listeExtension[extension] = listeExtension.get(extension, 0) + 1
	
	return listeExtension

# Fonction chargée de demander une information à l'utilisateur. Elle peut contraindre sa réponse à une liste définie.
# Elle renvoie sa réponse en tant que string
def demander_information_string(question: str, reponses_possibles: Optional[Set[str]] = None) -> str:
	if reponses_possibles is None:
		reponses_possibles = set() # Utilise un set vide si aucun n'est fourni

	reponse_utilisateur = ""
	
	reponses_possibles_upper = {r.upper().strip() for r in reponses_possibles}
	question = question + " (Rép. possibles : " + ", ".join(reponses_possibles) + "):".upper().strip()

	# On affiche la question et attends une réponse de l'utilisateur
	if len(reponses_possibles_upper) >= 1:

		# Tant que la réponse de l'utilisateur est invalide
		while reponse_utilisateur not in reponses_possibles_upper:
			sys.stdout.write(question + ' ') #On écrit puis affiche la question
			sys.stdout.flush()

			reponse_utilisateur = sys.stdin.readline().strip().upper()
			
			# Si la réponse de l'utilisateur est correcte, on sort de la boucle
			if reponse_utilisateur in reponses_possibles_upper:
				print(f"\r{question}{reponse_utilisateur}")
				break

			# On efface l'écran
			nombreCaractereAffiche = len(question) + len(reponse_utilisateur)
			sys.stdout.write('\r' + ' ' * (nombreCaractereAffiche + 1) + '\r')
			sys.stdout.flush()

			# On affiche un message d'erreur
			messageErreur = "Réponse invalide, veuillez réessayer"
			sys.stdout.write('\r' + messageErreur + '\r')
			sys.stdout.flush()
			time.sleep(2)

			# On efface de nouveau l'écran
			sys.stdout.write('\r' + ' ' * (len(messageErreur) + 1) + '\r')
			sys.stdout.flush()

	else:
		reponse_utilisateur = input(question).upper().strip()
	
	return reponse_utilisateur

# Fonction chargée de supprimer récursivement un dossier (indiquer le chemin relatif du dossier)
def supprimer_dossier(dossier_a_supprimer: str, recreer_dossier_vide: Optional[bool] = False) -> bool:
	dossier_a_supprimer = os.path.join(DOSSIER_PHOTO, dossier_a_supprimer)
	
	try:
		shutil.rmtree(dossier_a_supprimer)
		if recreer_dossier_vide: os.mkdir(dossier_a_supprimer)

		return True
	
	except OSError as e:
		print(f"Erreur lors de la suppression du dossier: {e}")
		return False

# Fonction chargée de stacker chacune des photos
def stacking_photos(liste_photos: List[str], dossier_temporaire: str, methode_stacking: str, nom_photo_finale: Optional[str] = "stacking"):
	from wand.image import Image

	# 
	extension_photo = os.path.splitext(liste_photos[0])[1]
	nom_photo_finale = f"{nom_photo_finale}{extension_photo}"
	chemin_photo_finale = os.path.join(dossier_temporaire, nom_photo_finale)

	# On fusionne les images par deux
	with Image(filename=liste_photos[0]) as image_base:
		for i in range(1, len(liste_photos)):
			with Image(filename=liste_photos[i]) as image_a_fusionner:
				# Pour chacune des fusions, on applique un coefficients sur la nouvelle image pour tenir compte des images déja fusionnées
				pourcentage = int(100 / (i + 1))
				image_base.composite(image_a_fusionner, operator='blend', arguments=str(pourcentage))
		
		image_base.save(filename=chemin_photo_finale)
		
		return nom_photo_finale

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
	
	# Definition des limites maximum de RAM et disque dur utilisable
	from wand.resource import limits

	limits['memory'] = TAILLE_MAX_RAM_GO_UTILISABLE * 1024 * 1024 * 1024
	limits['map'] = TAILLE_MAX_DISQUE_DUR_GO_UTILISABLE * 1024 * 1024 * 1024

	# Le dossier contenant les photos à traiter
	DOSSIER_PHOTO = os.path.abspath(sys.argv[1])
	listeExtension = compter_type_fichier(DOSSIER_PHOTO)

	# On vérifie qu'il n'y ait qu'un seul type de fichier image dans le dossier
	type_fichier_trouve = listeExtension.keys()
	type_image_trouve = EXTENSIONS_IMAGE.intersection(type_fichier_trouve)

	if len(type_image_trouve) > 1:
		print("Des fichiers images de différents type ont été trouvés, veuillez ne laisser qu'un seul type de fichier à traiter.")
		sys.exit(1)
	
	#############################################
	##### PREPARATION DU DOSSIER TEMPORAIRE #####
	#############################################
	DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS = "tmp"
	CHEMIN_DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS = os.path.join(DOSSIER_PHOTO, DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS)

	# Si le dossier temporaire existe déjà
	if DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS in os.listdir(DOSSIER_PHOTO):
#
#		# On pose la question à l'utilisateur
#		question = "Un dossier temporaire contenant les photos en cours de traitement a été trouvé.\n" \
#		"Si vous souhaitez poursuivre l'installation, ce dossier sera supprimé.\n" \
#		"\nVoulez-vous continuer ?"
#
#		reponse_accepte = {"O", "N"}
#		reponse_utilisateur = demander_information_string(question, reponse_accepte)
#
#		# Si l'utilisateur accepte la suppression du dossier temporaire
#		if reponse_utilisateur == 'O':
#			if not supprimer_dossier(DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS, True): sys.exit(1)
#
#		else:
#			print("Arrêt du script, veuillez déplacer ou supprimer ce dossier avant de relancer le script.")
#			sys.exit(1)

		# Suppression et recréation du dossier temporaire
		supprimer_dossier(DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS, True)
		
	# Si le dossier temporaire n'existe pas
	else: os.mkdir(CHEMIN_DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS)

	# On fait l'inventaire des photos présentes pour un traitement ultérieur
	liste_fichier = os.listdir(DOSSIER_PHOTO)
	liste_photos = []

	for fichier in liste_fichier:
		chemin_fichier = os.path.join(DOSSIER_PHOTO, fichier)
#		print(chemin_fichier)
		if os.path.isfile(chemin_fichier): liste_photos.append(chemin_fichier)

	# On appelle la fonction de stacking des photos
	from wand.exceptions import CacheError
	
	try:
		nom_fichier_final = stacking_photos(liste_photos, CHEMIN_DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS, 'mosaic')
		shutil.copy(os.path.join(CHEMIN_DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS, nom_fichier_final), os.path.join(DOSSIER_PHOTO, nom_fichier_final))
		supprimer_dossier(DOSSIER_TEMPORAIRE_TRAITEMENT_PHOTOS, False)

	except CacheError as e:
		print(f"Erreur lors du stacking, veuillez verifier les ressoures materielles (RAM, disque dur) disponible et celles allouees a ImageMagick.\n{e}")
		exit(1)
		
	
