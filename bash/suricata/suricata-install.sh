#!/bin/bash

## Reference is:
#https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Debian_Installation
##

isIPS=0

sudo aptitude install libpcre3 libpcre3-dbg libpcre3-dev \
build-essential autoconf automake libtool libpcap-dev libnet1-dev \
libyaml-0-2 libyaml-dev zlib1g zlib1g-dev libmagic-dev libcap-ng-dev \
libjansson-dev pkg-config -ry

if isIPS
then
	sudo aptitude install libnetfilter-queue-dev libnetfilter-queue1 \
	libnfnetlink-dev libnfnetlink0 -ry
fi

wget http://www.openinfosecfoundation.org/download/suricata-2.0.5.tar.gz
tar -xvzf suricata-2.0.5.tar.gz
cd suricata-2.0.5

#DEFAULT install: IDS
if isIPS
then
	./configure --enable-nfqueue --prefix=/usr --sysconfdir=/etc --localstatedir=/var
else
	./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var
fi

make
sudo make install-full

# Make sure the existing list with libraries will be updated with the new library
sudo ldconfig

#You can now start suricata by running as root something like '/usr/bin/suricata -c /etc/suricata//suricata.yaml -i eth0'.

#If a library like libhtp.so is not found, you can run suricata with:
#'LD_LIBRARY_PATH=/usr/lib /usr/bin/suricata -c /etc/suricata//suricata.yaml -i eth0'.

#While rules are installed now, it's highly recommended to use a rule manager for maintaining rules.
#The two most common are Oinkmaster and Pulledpork. For a guide see:
#https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Rule_Management_with_Oinkmaster

echo 'config reference: osvdb		http://osvdb.org
' | sudo tee -a /etc/suricata/reference.config

echo "To start Suricata's engine"
echo "sudo suricata -c /etc/suricata/suricata.yaml -i <your favorite interface> --init-errors-fatal"