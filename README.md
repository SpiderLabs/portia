# portia

Portia aims to automate a number of techniques commonly performed on internal network penetration tests after a low privileged account has been compromised
- Privilege escalation
- Lateral movement
- Convenience modules

Portia is a genus of jumping spider that feeds on other spiders - known for their intelligent hunting behaviour and problem solving capabilities usually only found in larger animals
  
#Slides   
https://docs.google.com/presentation/d/1x_1bjCCD5hwJFWzlHM0lEPOHdWUlfYgjkUYBtdBFEmM/pub?start=false&loop=false&delayms=3000  

#Videos (Will be adding more soon)  
Video that shows privilege escalation via impersonation tokens and running of post exploitation modules  
https://asciinema.org/a/45ry3g26devqcabpugwyz4to5  

#Dependencies
```
pip install pysmb tabulate termcolor xmltodict impacket

apt install autoconf automake autopoint libtool pkg-config
mkdir /pentest
cd/pentest
git clone https://github.com/libyal/libesedb.git
cd libesedb
./synclibs.sh
./autogen.sh
cd /pentest
git clone https://github.com/csababarta/ntdsxtract
cd ntdsxtract
python setup.py install
```
