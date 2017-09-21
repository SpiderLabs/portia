#!/usr/bin/env python
import time
import sys
import os
import cmd
import argparse
import ConfigParser
import logging
import string
import random
from threading import Thread

from impacket.examples import logger
from impacket import version, smbserver
from impacket.smbconnection import *
from impacket.dcerpc.v5 import transport, scmr

OUTPUT_FILENAME = '__output'
BATCH_FILENAME  = 'execute.bat'
SMBSERVER_DIR   = '__tmp'
DUMMY_SHARE     = 'TMP'
results=''


class CMDEXEC:
    def __init__(self, username='', password='', domain='', hashes=None, aesKey=None,
                 doKerberos=None, kdcHost=None, mode=None, share=None, port=445, command=None):
	self.__command = command
        self.__username = username
        self.__password = password
        self.__port = port
        #self.__serviceName = 'BTOBTO12'
	self.__serviceName = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
        self.__domain = domain
        self.__lmhash = ''
        self.__nthash = ''
        self.__aesKey = aesKey
        self.__doKerberos = doKerberos
        self.__kdcHost = kdcHost
        self.__share = share
        self.__mode  = mode
        self.shell = None
        if hashes is not None:
            self.__lmhash, self.__nthash = hashes.split(':')

    def getOutput(self):
	return results

    def run(self, remoteName, remoteHost):
        stringbinding = 'ncacn_np:%s[\pipe\svcctl]' % remoteName
        logging.debug('StringBinding %s'%stringbinding)
        rpctransport = transport.DCERPCTransportFactory(stringbinding)
        rpctransport.set_dport(self.__port)
        rpctransport.setRemoteHost(remoteHost)
        if hasattr(rpctransport,'preferred_dialect'):
            rpctransport.preferred_dialect(SMB_DIALECT)
        if hasattr(rpctransport, 'set_credentials'):
            rpctransport.set_credentials(self.__username, self.__password, self.__domain, self.__lmhash,
                                         self.__nthash, self.__aesKey)
        rpctransport.set_kerberos(self.__doKerberos, self.__kdcHost)

        self.shell = None
        try:
        	self.shell = RemoteShell(self.__share, rpctransport, self.__mode, self.__serviceName, self.__command)
		self.shell.onecmd(self.__command)
		#self.shell.finish()
		rpctransport.disconnect()
		#print self.shell.get_output()
		#last
	except Exception as e:
	    #except  (Exception, KeyboardInterrupt), e:
            #import traceback
            #traceback.print_exc()
	    #print "heretest1"
	    if "STATUS_SHARING_VIOLATION" not in str(e):
	        logging.critical(str(e))
            if self.shell is not None:
                self.shell.finish()
            sys.stdout.flush()
	    try:
		    rpctransport.disconnect()
	    except Exception as f:
		    pass
		    #logging.critical(str(f))
	    #print "exit123"
	    #return None
	    #os._exit(1)
            #sys.exit(1)
	    #pass	

class RemoteShell(cmd.Cmd):
    #def __init__(self, share, rpc, mode, serviceName):
    def __init__(self, share, rpc, mode, serviceName, command):
        cmd.Cmd.__init__(self)
        self.__share = share
        self.__mode = mode
        self.__output = '\\\\127.0.0.1\\' + self.__share + '\\' + OUTPUT_FILENAME
        self.__batchFile = '%TEMP%\\' + BATCH_FILENAME 
        self.__outputBuffer = ''
        self.__command = command
        self.__shell = '%COMSPEC% /Q /c '
        self.__serviceName = serviceName
        self.__rpc = rpc
        self.intro = '[!] Launching semi-interactive shell - Careful what you execute'

        self.__scmr = rpc.get_dce_rpc()
	#self.__scmr.disconnect()
	found=False
	while found==False:
         try:
            self.__scmr.connect()
	    found=True
         except Exception, e:
	    #print "heretest2"
	    #[Errno Connection error (172.16.126.132:62699)] [Errno 61] Connection refused
            #logging.critical(str(e))
	    if "The NETBIOS connection with the remote host timed out." in str(e) or "Connection reset by peer" in str(e) or "Connection error" in str(e):
            	#self.__scmr.disconnect()
		pass
	    else:
 	        os._exit(1)
	    #pass
        s = rpc.get_smb_connection()

        # We don't wanna deal with timeouts from now on.
        s.setTimeout(100000)

        self.__scmr.bind(scmr.MSRPC_UUID_SCMR)
        resp = scmr.hROpenSCManagerW(self.__scmr)
        self.__scHandle = resp['lpScHandle']
        self.transferClient = rpc.get_smb_connection()
        self.do_cd('')
        #last
	#self.execute_remote(command)

	#global results
	#results = self.__outputBuffer
        #print "xxx3: "+self.__outputBuffer

    def finish(self):
        # Just in case the service is still created
        try:
           self.__scmr = self.__rpc.get_dce_rpc()
           self.__scmr.connect() 
           self.__scmr.bind(scmr.MSRPC_UUID_SCMR)
           resp = scmr.hROpenSCManagerW(self.__scmr)
           self.__scHandle = resp['lpScHandle']
           resp = scmr.hROpenServiceW(self.__scmr, self.__scHandle, self.__serviceName)
	   service = resp['lpServiceHandle']
           scmr.hRDeleteService(self.__scmr, service)
           scmr.hRControlService(self.__scmr, service, scmr.SERVICE_CONTROL_STOP)
           scmr.hRCloseServiceHandle(self.__scmr, service)
        except Exception as e:
	   #print "here10: "+str(e)
           pass

    def do_shell(self, s):
        os.system(s)

    #def onecmd(self, s):
    #    stop = None
    #	#s = self.precmd(s)
    #    #stop = self.onecmd(s)
    #	print "running onecmd"
    #    stop = self.postcmd(stop, s)
    # 	#self.postloop()
    #	return None

    #def precmd(self, s):	
    #	return s

    #def postcmd(self, stop, s):
    #    return stop
   
    #def postloop(self):
    #	pass

    #def do_exit(self, s):
    #    return True

    def do_EOF(self, s):
	return True

    def emptyline(self):
        return False

    def do_cd(self, s):
        # We just can't CD or mantain track of the target dir.
        if len(s) > 0:
            logging.error("You can't CD under SMBEXEC. Use full paths.")

        self.execute_remote('cd ' )
        if len(self.__outputBuffer) > 0:
            # Stripping CR/LF
            self.prompt = string.replace(self.__outputBuffer,'\r\n','') + '>'
            self.__outputBuffer = ''

    def do_CD(self, s):
        return self.do_cd(s)

    def default(self, line):
        if line != '':
            self.send_data(line)

    def get_output(self):
        def output_callback(data):
            self.__outputBuffer += data

        if self.__mode == 'SHARE':
            self.transferClient.getFile(self.__share, OUTPUT_FILENAME, output_callback)
            self.transferClient.deleteFile(self.__share, OUTPUT_FILENAME)        

    def execute_remote(self, data):
        command = self.__shell + 'echo ' + data + ' ^> ' + self.__output + ' 2^>^&1 > ' + self.__batchFile + ' & ' + \
                  self.__shell + self.__batchFile
        if self.__mode == 'SERVER':
            command += ' & ' + self.__copyBack
        command += ' & ' + 'del ' + self.__batchFile 

        logging.debug('Executing %s' % command)
        resp = scmr.hRCreateServiceW(self.__scmr, self.__scHandle, self.__serviceName, self.__serviceName,
                                     lpBinaryPathName=command, dwStartType=scmr.SERVICE_DEMAND_START)
        service = resp['lpServiceHandle']

        try:
           scmr.hRStartServiceW(self.__scmr, service)
        except:
           pass
        scmr.hRDeleteService(self.__scmr, service)
        scmr.hRCloseServiceHandle(self.__scmr, service)
        self.get_output()

    def send_data(self, data):
        self.execute_remote(data)
	global results
	results = self.__outputBuffer
    	#print self.__outputBuffer
        self.__outputBuffer = ''
	self.finish()
	
# Process command-line arguments.
if __name__ == '__main__':
    # Init the example's logger theme
    logger.init()
    print version.BANNER

    parser = argparse.ArgumentParser()

    parser.add_argument('target', action='store', help='[[domain/]username[:password]@]<targetName or address>')
    parser.add_argument('-share', action='store', default = 'C$', help='share where the output will be grabbed from '
                                                                       '(default C$)')
    parser.add_argument('-mode', action='store', choices = {'SERVER','SHARE'}, default='SHARE',
                        help='mode to use (default SHARE, SERVER needs root!)')
    parser.add_argument('-debug', action='store_true', help='Turn DEBUG output ON')

    group = parser.add_argument_group('connection')

    group.add_argument('-dc-ip', action='store',metavar = "ip address", help='IP Address of the domain controller. '
                       'If ommited it use the domain part (FQDN) specified in the target parameter')
    group.add_argument('-target-ip', action='store', metavar="ip address", help='IP Address of the target machine. If '
                       'ommited it will use whatever was specified as target. This is useful when target is the NetBIOS '
                       'name and you cannot resolve it')
    group.add_argument('-port', choices=['139', '445','63608','61110'], nargs='?', default='445', metavar="destination port",
                       help='Destination port to connect to SMB Server')

    group = parser.add_argument_group('authentication')

    group.add_argument('-hashes', action="store", metavar = "LMHASH:NTHASH", help='NTLM hashes, format is LMHASH:NTHASH')
    group.add_argument('-no-pass', action="store_true", help='don\'t ask for password (useful for -k)')
    group.add_argument('-k', action="store_true", help='Use Kerberos authentication. Grabs credentials from ccache file '
                       '(KRB5CCNAME) based on target parameters. If valid credentials cannot be found, it will use the '
                       'ones specified in the command line')
    group.add_argument('-aesKey', action="store", metavar = "hex key", help='AES key to use for Kerberos Authentication '
                                                                            '(128 or 256 bits)')

 
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    options = parser.parse_args()

    if options.debug is True:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    import re
    domain, username, password, remoteName = re.compile('(?:(?:([^/@:]*)/)?([^@:]*)(?::([^@]*))?@)?(.*)').match(options.target).groups('')

    #In case the password contains '@'
    if '@' in remoteName:
        password = password + '@' + remoteName.rpartition('@')[0]
        remoteName = remoteName.rpartition('@')[2]

    if domain is None:
        domain = ''

    if password == '' and username != '' and options.hashes is None and options.no_pass is False and options.aesKey is None:
        from getpass import getpass
        password = getpass("Password:")
	
    if options.target_ip is None:
        options.target_ip = remoteName

    if options.aesKey is not None:
        options.k = True

    try:
	command='ipconfig /all'
        executer = CMDEXEC(username, password, domain, options.hashes, options.aesKey, options.k,
                           options.dc_ip, options.mode, options.share, int(options.port),  command)
        executer.run(remoteName, options.target_ip)
	sys.exit(0)
    except Exception, e:
        logging.critical(str(e))
    sys.exit(0)
