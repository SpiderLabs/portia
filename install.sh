#!/bin/sh
#Contributed by @jivoi 

apt-get update
apt-get install -y autoconf automake autopoint libtool pkg-config

virtualenv -p python2 portia
source portia/bin/activate
pip install pysmb tabulate termcolor xmltodict pyasn1 pycrypto pyOpenSSL dnspython netaddr

ln -sf /opt /pentest

cd /opt
git clone https://github.com/CoreSecurity/impacket
python setup.py install

cd /opt
git clone https://github.com/libyal/libesedb.git && cd libesedb
./synclibs.sh
./autogen.sh

cd /opt
git clone https://github.com/csababarta/ntdsxtract && cd ntdsxtract
python setup.py install

cd /opt
git clone https://github.com/milo2012/portia.git && cd portia
./portia.py
