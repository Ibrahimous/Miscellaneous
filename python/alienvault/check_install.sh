#!/bin/bash

sudo apt-get update && sudo aptitude upgrade -ry
sudo aptitude install python-pip -ry
sudo pip install requests