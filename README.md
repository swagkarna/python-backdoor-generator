# simple-backdoor-generator



## About

Simple-backdoor-generator is a TCP backdoor generator written in Python 3.8.0.

It generates the payload in a .py and .exe format.

## Setup
You need to install Python 3.8.0 or higher.

Now you need to navigate to the project directory for example in windows:

```
cd C:\Users\<Your User>\<Path to the project>\python-backdoor-generator\simple-backdoor-generator
```

All the libs are saved in the requirements.txt file.
You can install them with typing:

```
pip install requierments.txt
```


Now you are good to go.

## Usage
If you just want to start an listener need to type in your project directory:

```
python main.py --PORT <Your Port to listen on> --HOST <Optional your ip> 
```

Then it should look like this:

![](\media\ConsoleListening.png)

If you want to build your payload too you type:

```
 python main.py --PORT <Port to listen on> --BUILD 
```

When this doesn't work try typing:

```
python3 main.py <Your arguments> 
```

Or installing the libs manual by typing :

```
pip install datetime
pip install socket
pip install pyinstaller
pip install argparse
pip install subprocess
```

If you are on linux try installing pyinstaller per your package manager

If you want it in just one command:

```
pip install datetime && pip install socket && pip install https://github.com/pyinstaller/pyinstaller/archive/develop.tar.gz && pip install argparse && pip install subprocess
```

