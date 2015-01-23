#!/bin/bash

sudo apt-get update && sudo aptitude upgrade -ry && sudo aptitude install -yq python-setuptools build-essential libmagic-dev libpcre3-dev libpcap-dev python-dev git-core autoconf automake libpcre3 libtool python swig gcc

git clone https://github.com/MITRECND/chopshop.git && cd chopshop

sudo pip install pymongo M2Crypto pycrypto dnslib && \
sudo apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install pynids and remove install dir after to conserve space
cd /tmp/ && \
git clone --recursive git://github.com/MITRECND/pynids && \
cd pynids && \
python setup.py build && \
python setup.py install && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install htpy and remove install dir after to conserve space
cd /tmp/ && \
git clone --recursive git://github.com/MITRECND/htpy && \
cd htpy && \
python setup.py build && \
python setup.py install && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install yaraprocessor and remove install dir after to conserve space
cd /tmp/ && \
git clone git://github.com/MITRECND/yaraprocessor.git && \
cd yaraprocessor && \
python setup.py install && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install pylibemu and remove install dir after to conserve space
cd /tmp/ && \
git clone git://git.carnivore.it/libemu.git && \
cd libemu && autoreconf -v -i && \
./configure --enable-python-bindings --prefix=/opt/libemu && \
make install && \
echo "/opt/libemu/lib/" >> /etc/ld.so.conf.d/libemu.conf && \
ldconfig && \
git clone git://github.com/buffer/pylibemu.git && \
cd pylibemu && \
echo /opt/libemu/lib > /etc/ld.so.conf.d/pylibemu.conf && \
python setup.py build && \
python setup.py install && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install ChopShop and remove install dir after to conserve space
cd /tmp/ && \
git clone --recursive git://github.com/MITRECND/chopshop && \
cd chopshop && \
make && \
make install && \
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*