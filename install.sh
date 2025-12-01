#!/bin/bash

# Package to install
IMAGEMAGICK_PKG="imagemagick"
PYTHON="python3 python3-pip"
WAND="libmagickwand-dev python3-wand"

# Update package lists and install packages
apt-get update --yes
apt-get upgrade --yes
apt-get install --yes $IMAGEMAGICK_PKG $WAND $PYTHON

# Install Wand Python library
python3 -m pip install Wand