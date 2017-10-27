# portia

Portia aims to automate a number of techniques commonly performed on internal network penetration tests after a low privileged account has been compromised
- Privilege escalation
- Lateral movement
- Convenience modules

Portia is a genus of jumping spider that feeds on other spiders - known for their intelligent hunting behaviour and problem solving capabilities usually only found in larger animals
  
A new functionality has been added.  The new script is 'hopandhack.py'.  
The new script ‘hopandhack‘ can be used by attackers to automatic find and hunt hosts that are not directly accessible from the attacker’s machine.  In some organizations, IT administrators have to use something called a ‘jump box’ or VPN to access the secure data centre or PCI network where sensitive data are stored.  
  
The ‘hopandhack’ script automates the process of finding hosts with the necessary routes to these secure network and compromises them.  The functionality of hopandhack will be incorporated into Portia in the next week or so.  
More details about the hopandhack script can be found at https://milo2012.wordpress.com/2017/09/21/jumping-from-corporate-to-compromising-semi-isolated-network/  
  
## Slides
https://www.slideshare.net/secret/tkQFhYeFY3zEi4  
  
## Videos (Will be adding more soon)  
Video that shows privilege escalation via impersonation tokens and running of post exploitation modules  
https://asciinema.org/a/45ry3g26devqcabpugwyz4to5  

## Dependencies

```
apt-get update
apt-get install -y autoconf automake autopoint libtool pkg-config freetds-dev
pip install pysmb tabulate termcolor xmltodict pyasn1 pycrypto pyOpenSSL dnspython netaddr python-nmap
cd /opt
git clone https://github.com/CoreSecurity/impacket
python setup.py install
cd /opt
git clone https://github.com/libyal/libesedb.git && cd libesedb
./synclibs.sh
./autogen.sh
./configure 
make
make install
ldconfig
cd /opt
git clone https://github.com/csababarta/ntdsxtract && cd ntdsxtract
python setup.py install
pip install git+https://github.com/pymssql/pymssql.git
cd /opt
git clone https://github.com/volatilityfoundation/volatility && cd volatility
python setup.py install
cd /opt
git clone https://github.com/SpiderLabs/portia
```
  
## How Portia Works
```

                        #7 Use Impersonation Token
                +------Run Mimikatz on DC---------------+   +---------------------------------------------------------+
                |      Dump Password Hashes from DC     |   |                                                         |
                |                                       |   |                                                         |
+------------+  |     +-------------+                +--v---v-----+                                                   |
|Workstation |  |     | Workstation |                | Domain     |        #3 Checks if Account                       |
|(Workgroup) |  |     | (Domain)    |                | Controller | <------is in Domain Admin Group                   |
++---+-------+  |     +-+----+------+                +------+-----+                           |                       |
 ^   ^          |       ^    ^                              ^                                 |                       |
 |   |          |       |    |                              |                                 |                       |
 |   |          |       |    |                          #4 Check SYSVOL                   #2 Enumerate Users          |
 |   |          |       |    |                          for Passwords                     in Domain Admin Group       |
 |   |#6 Checks for     | #5 Checks if account              |                                 |                       |
 |   |Impersonation     | has admin rights          +-------+------+                          |                       |
 |   +Tokens--------------on host-------------------+  Hacker      +-------#1 Checks----------+                       |
 |                      |                           +----+---+-----+       credentials                                |
 |                      |                                |   |                                                        |
 |                      |                                |   |                                                        |
 |                      |                                |   |                                                        |
 |           #8 Use New Hashes / Passwords               |   +--------------------------------------------------------+
 +-----------to Compromise Other Hosts-------------------+
```
