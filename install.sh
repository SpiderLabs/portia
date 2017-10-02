#!/bin/sh
#Contributed by @jivoi 

apt-get update
apt-get install -y autoconf automake autopoint libtool pkg-config freetds-dev 

virtualenv -p python2 portia
source portia/bin/activate
pip install pysmb tabulate termcolor xmltodict pyasn1 pycrypto pyOpenSSL dnspython netaddr python-nmap 

ln -sf /opt /pentest

cd /opt
git clone https://github.com/CoreSecurity/impacket && cd impacket
python setup.py install

cd /opt
git clone https://github.com/libyal/libesedb.git && cd libesedb
./synclibs.sh
./autogen.sh

cd /opt
git clone https://github.com/csababarta/ntdsxtract && cd ntdsxtract
python setup.py install

sudo pip install git+https://github.com/pymssql/pymssql.git

cd /opt
git clone https://github.com/volatilityfoundation/volatility && cd volatility
python setup.py install

cd /opt
git clone https://github.com/SpiderLabs/portia.git && cd portia
git submodule init && git submodule update --recursive
./portia.py

