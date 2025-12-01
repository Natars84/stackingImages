#!/bin/bash

# Package to install
IMAGEMAGICK_PKG="imagemagick"
PYTHON="python3"
WAND="libmagickwand-dev python-wand"

# Update package lists and install packages
apt-get update --yes
apt-get upgrade --yes
apt-get install --yes $IMAGEMAGICK_PKG $WAND $PYTHON

# Install pip for Python 3
python -m ensurepip --upgrade
wget https://bootstrap.pypa.io/get-pip.py | $PYTHON

# Install Wand Python library
$PYTHON -m pip install Wand