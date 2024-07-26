#!/bin/bash

#Thanks https://github.com/joyent/node/wiki/installing-node.js-via-package-manager#debian-and-ubuntu-based-linux-distributions

sudo aptitude install -ry curl
curl -sL https://deb.nodesource.com/setup | sudo bash -
sudo aptitude install -ry nodejs