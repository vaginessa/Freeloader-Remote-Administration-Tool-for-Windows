from distutils.core import setup
import py2exe,sys,os,config


sys.argv.append('py2exe')

Botversion = config.BOTVERSION
name = config.name
description = config.description
author = config.author
author_email = config.author_email

setup(
    name=name,
    version=Botversion,
    description=description,           
    author=author,
    author_email=author_email,
    options = {'py2exe': {'bundle_files': 1, 'compressed': True, 'dll_excludes' : ["MSVCP90.DLL"]}},
    windows = [{'script': "Main.py"}],   
    zipfile = None,
)


