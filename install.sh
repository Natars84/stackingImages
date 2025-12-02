#!/bin/bash

# Chemin par défaut pour l'environnement virtuel
VENV_DIR_PAR_DEFAUT="./venv"

# Récupération du chemin de l'environnement virtuel depuis les arguments ou utilisation du chemin par défaut
VENV_DIR="${1:-$VENV_DIR_PAR_DEFAUT}"

# Paquets système à installer
IMAGEMAGICK_PKG="imagemagick"
PYTHON="python3 python3-pip python3-venv"
WAND_SYSTEME="libmagickwand-dev"

# Dépendances Python à installer
WAND_PYTHON="Wand"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Démarrage de l'installation de l'application (script GitHub)."

# Mise à jour et installation des paquets système
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Mise à jour des index APT et mise à niveau du système."
apt-get update --yes && apt-get upgrade --yes

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Installation des dépendances APT: $IMAGEMAGICK_PKG $PYTHON $WAND_SYSTEME"
if ! apt-get install --yes $IMAGEMAGICK_PKG $PYTHON $WAND_SYSTEME --fix-missing; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERREUR] Échec de l'installation des dépendances système."
    exit 1
fi

# Création de l'environnement virtuel Python
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Création de l'environnement virtuel Python dans $VENV_DIR."

if ! python3 -m venv "$VENV_DIR"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERREUR] Échec de la création de l'environnement virtuel."
    exit 1
fi

# Installation des dépendances Python dans le VENV
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Installation de la librairie $WAND_PYTHON dans le VENV."

if ! "$VENV_DIR/bin/pip" install "$WAND_PYTHON"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERREUR] Échec de l'installation de la librairie Python Wand."
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Installation terminée avec succès."