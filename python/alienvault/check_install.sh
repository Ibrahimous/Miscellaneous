#!/bin/bash

echo "Updating your system"
sudo apt-get update && sudo aptitude upgrade -ry

echo "Installing git & python"
sudo aptitude install git python-dev -ry

echo "Installing pip"
sudo aptitude install python-pip -ry

echo "Installing the \"requests\" module"
sudo pip install requests