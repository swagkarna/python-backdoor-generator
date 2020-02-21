# !/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This fie contains the main class for the module
'''

# TODO : Document code
# TODO : Write README.md

__author__ = 'lorem.cookie'
__version__ = '0.2/alpha'

#Native Libs
import os
import warnings
from datetime import datetime

#Not native Libs
import colorama

class FileOnlyModule(Exception):
    def __init__(self):
        Exception.__init__(self,'FILE IS ONLY A MODULE')
        
class LogFileError(Exception):
    def __init__(self):
        Exception.__init__(self,'ERROR OPENING LOG FILE')
        
class LogDirError(Exception):
    def __init__(self):
        Exception.__init__(self,'ERROR OPENING LOG DIR')
        
class LogLevelError(Exception):
    def __init__(self):
        Exception.__init__(self,'LogLevel VAR MUST BE : WARNING, ERROR, INFO or DEBUG')
        
class NoLogLevel(Exception):
    def __init__(self):
        Exception.__init__(self,'LogLevel MUST BE SPECIFIED WHEN LOG FUNCTION IS CALLED')
        
class logging:
    
    def __init__(self, LogLevel=None, LogFile='LogFile.log', LogDir='Log', color=False, PrintFeedback=False, Debug=False):
        
        #Define Variabels
        self.time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #Get System time and format it
        self.LogFile = LogFile
        self.LogDir = LogDir
        self.Debug = Debug
        self.LogLevel = LogLevel
        self.color = color
        self.PrintFeedback = PrintFeedback
        LogDir = os.path.join(os.getcwd(), self.LogDir)
        self.LogDir = LogDir
        LogFile = os.path.join(self.LogDir, self.LogFile)
        self.LogFile = LogFile
        
        if self.color and not self.PrintFeedback:
            
            warnings.warn('\nColor set to True and not PrintFeedback to False Color wont do anything\n')
        
        if self.color:
            
            colorama.init()
            self.BLUE = colorama.Fore.BLUE
            self.RED = colorama.Fore.RED
            self.YELLOW = colorama.Fore.YELLOW
            self.BLUE = colorama.Fore.BLUE
            self.MAGENTA = colorama.Fore.MAGENTA
            self.RESET = colorama.Fore.RESET
        
        if self.Debug and not self.color:
            
            print('[INFO] Check if {} exists...'.format(self.LogDir))
        
        if self.Debug and self.color:
            
            print('{}[INFO] Check if {} exists...{}'.format(self.BLUE, self.LogDir, self.RESET))
                    
        if os.path.isdir(self.LogDir):
            
            if self.Debug and not self.color:
                
                print('[INFO] {} Does exist'.format(self.LogDir))
                
            if self.Debug and self.color:
                
                print('{}[INFO] {} Does exist{}'.format(self.BLUE, self.LogDir, self.RESET))
                
        else:
            
            if self.Debug and not self.color:
                
                print('[WARNING] {} Does not exist'.format(self.LogDir))
                print('[INFO] {} Creating dir'.format(self.LogDir))
                
            if self.Debug and self.color:
                
                print('{}[WARNING] {} Does not exist{}'.format(self.YELLOW, self.LogDir, self.RESET))
                print('{}[INFO] {} Creating dir{}'.format(self.BLUE, self.LogDir, self.RESET))
                
            try:
                
                os.mkdir(self.LogDir)
                
            except FileExistsError:
                
                if self.Debug and not self.color:
                    
                    print('[INFO] Error creating {}'.format(self.LogDir))
                    print('[WARNING] Exiting Program...')
                                
                if self.Debug and self.color:
                        
                    print('{}[INFO] Error creating {}{}'.format(self.BLUE, self.LogDir, self.RESET))
                    print('{}[WARNING] Exiting Program...{}'.format(self.YELLOW, self.RESET))
                    
                raise LogDirError

        if self.Debug and not self.color:
            
            print('[INFO] Check if {} exists...'.format(self.LogFile))
        
        if self.Debug and self.color:
            
            print('{}[INFO] Check if {} exists...{}'.format(self.BLUE, self.LogFile ,self.RESET))
        
        if os.path.isfile(self.LogFile):
            
            if self.Debug and not self.color:
                
                print('[INFO] {} Does exist'.format(self.LogFile))
                
            if self.Debug and self.color:
                
                print('{}[INFO] {} Does exist{}'.format(self.BLUE, self.LogFile, self.RESET))
            
        else:
            
            if self.Debug and not self.color:
                
                print('[WARNING] {} Does not exist'.format(self.LogFile))
                print('[INFO] {} Creating file'.format(self.LogFile))
                
            if self.Debug and self.color:
                
                print('{}[WARNING] {} Does not exist{}'.format(self.YELLOW, self.LogFile, self.RESET))
                print('{}[INFO] {} Creating file{}'.format(self.BLUE, self.LogFile, self.RESET))
            
            try:
                
                open(self.LogFile, 'a').close()
                
            except (IOError, OSError):
                
                if self.Debug and not self.color:
                    
                    print('[ERROR] Error creating {}'.format(self.LogDir))
                    print('[WARNING] Exiting Program...')
                    
                if self.Debug and self.color:
                    
                    print('{}[ERROR] Error creating {}{}'.format(self.RED, self.LogDir, self.RESET))
                    print('{}[WARNING] Exiting Program...{}'.format(self.YELLOW, self.RESET))
                
                raise LogFileError
            
    def LOG(self, inputstr):
        
        if(self.LogLevel == 'WARNING'):
            
            self.LogLevel = 'WARNING'
            
        elif(self.LogLevel == 'ERROR'):
            
            self.LogLevel = 'ERROR'
            
        elif(self.LogLevel == 'DEBUG'):
            
            self.LogLevel = 'DEBUG'
            
        elif(self.LogLevel == 'INFO'):
            
            self.LogLevel = 'INFO'
            
        elif(self.LogLevel == None):
            
            raise NoLogLevel
        
        else:
            
            raise LogLevelError
        
        if self.PrintFeedback and not self.color:
            
            print('[{}]{}\n'.format(self.LogLevel, inputstr))
                
        if self.PrintFeedback and self.color:
            
            if(self.LogLevel == 'WARNING'):
                
                print('{}[{}]{}{}\n'.format(self.YELLOW, self.LogLevel, inputstr, self.RESET))
            
            elif(self.LogLevel == 'ERROR'):
                
                print('{}[{}]{}{}\n'.format(self.RED, self.LogLevel, inputstr, self.RESET))
            
            elif(self.LogLevel == 'DEBUG'):
                
                print('{}[{}]{}{}\n'.format(self.BLUE, self.LogLevel, inputstr, self.RESET))
            
            elif(self.LogLevel == 'INFO'):
                
                print('{}[{}]{}{}\n'.format(self.BLUE, self.LogLevel, inputstr, self.RESET))
                
        try:
            
            with open(self.LogFile, 'a') as f:
                
                f.write('[{}]({}){}\n'.format(str(self.LogLevel), str(self.time_now), str(inputstr)))
                
        except (IOError, OSError):
            
            raise LogFileError
                
    def OK(self, inputstr):
        
        if self.PrintFeedback and not self.color:
            
            print('[OK]{}'.format(inputstr))
            
        if self.PrintFeedback and self.color:
            
            print('{}[OK]{}{}'.format(self.GREEN, inputstr, self.RESET))
            
        try:
            
            with open(self.LogFile, 'a') as f:
                
                f.write('[OK]({}){}'.format(str(self.time_now), str(inputstr)))
                
        except (IOError, OSError):
            
            raise LogFileError
        
    def INFO(self, inputstr):
        
        if self.PrintFeedback and not self.color:
            
            print('[INFO]{}'.format(inputstr))
            
        if self.PrintFeedback and self.color:
            
            print('{}[INFO]{}{}'.format(self.BLUE, inputstr, self.RESET))
            
        try:
            
            with open(self.LogFile, 'a') as f:
                
                f.write('[INFO]({}){}\n'.format(str(self.time_now), str(inputstr)))
                
        except (IOError, OSError):
            
            raise LogFileError
        
    def WARNING(self, inputstr):
        
        if self.PrintFeedback and not self.color:
            
            print('[WARNING]{}'.format(inputstr))
            
        if self.PrintFeedback and self.color:
            
            print('{}[WARNING]{}{}'.format(self.YELLOW, inputstr, self.RESET))
            
        try:
            
            with open(self.LogFile, 'a') as f:
                
                f.write('[WARNING]({}){}\n'.format(str(self.time_now), str(inputstr)))
                
        except (IOError, OSError):
            
            raise LogFileError
        
    def ERROR(self, inputstr):
        
        if self.PrintFeedback and not self.color:
            
            print('[ERROR]{}'.format(inputstr))
            
        if self.PrintFeedback and self.color:
            
            print('{}[ERROR]{}{}'.format(self.RED, inputstr, self.RESET))
            
        try:
            
            with open(self.LogFile, 'a') as f:
                
                f.write('[ERROR]({}){}\n'.format(str(self.time_now), str(inputstr)))
                
        except (IOError, OSError):
            
            raise LogFileError
        
    def DEBUG(self, inputstr):
        
        if self.PrintFeedback and not self.color:
            
            print('[DEBUG]{}'.format(inputstr))
            
        if self.PrintFeedback and self.color:
            
            print('{}[DEBUG]{}{}'.format(self.MAGENTA, inputstr, self.RESET))
            
        try:
            
            with open(self.LogFile, 'a') as f:
                
                f.write('[DEBUG]({}){}\n'.format(str(self.time_now), str(inputstr)))
                
        except (IOError, OSError):
            
            raise LogFileError
        
if __name__ == '__main__':
    
    raise FileOnlyModule