#!/bin/bash

# Paquets système à installer
IMAGEMAGICK_PKG="imagemagick"
PYTHON="python3 python3-pip"
WAND_SYSTEME="libmagickwand-dev"

# Dépendances Python à installer
WAND_PYTHON="Wand"

# Dossier pour l'environnement virtuel
VENV_DIR="./venv"

# Mise à jour et installation des paquets système
apt-get update --yes && apt-get upgrade --yes

echo "Installation des dépendances APT: $IMAGEMAGICK_PKG $PYTHON $WAND_DEPS"
if ! apt-get install --yes $IMAGEMAGICK_PKG $PYTHON $WAND_DEPS --fix-missing; then
    echo "ERREUR: Échec de l'installation des dépendances système."
    exit 1
fi

# Création de l'environnement virtuel Python
echo "Création de l'environnement virtuel Python dans $VENV_PATH."

if ! python3 -m venv "$VENV_PATH"; then
    echo "ERREUR: Échec de la création de l'environnement virtuel."
    exit 1
fi

# Installation des dépendances Python dans le VENV
echo "Installation de la librairie $WAND_PYTHON dans le VENV."

if ! "$VENV_PATH/bin/pip" install "$WAND_PYTHON"; then
    echo "ERREUR: Échec de l'installation de la librairie Python Wand."
    exit 1
fi

echo "Installation terminée avec succès."