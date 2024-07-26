# Install ChopShop Required Dependencies

apt-get -qq update && \
aptitude install -yr python-setuptools \
                      build-essential \
                      libmagic-dev \
                      libpcre3-dev \
                      libpcap-dev \
                      python-dev \
                      git-core \
                      autoconf \
                      automake \
                      libpcre3 \
                      libtool \
                      python \
                      swig

pip install pymongo && \
pip install M2Crypto && \
pip install pycrypto && \
pip install dnslib

apt-get clean

wget https://github.com/MITRECND/pynids/archive/master.zip
unzip master.zip
cd pynids-master
python setup.py build && sudo python setup.py install