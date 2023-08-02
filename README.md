# Tutorial API

## 1. Installation
### 1.1 Install Python 3 on Ubuntu and Python Virtual Environment.

Open the terminal (shell for Linux, or cmd for Windows), then use the respective commands bellow.

For Python :

(Linux)

```sh
sudo apt-get install python3
```

(Windows)

```sh 
https://www.python.org/downloads/windows/
```

For Python Venv :

(Linux)

```sh
sudo apt-get install python3-venv
```

(Windows)

```sh
pip install virtualenv
```

### 1.1.5 Clone the git repository

Clone git repository

(Git bash)

```sh
git clone git@github.com:AltaoBE/IA_Biologie.git
```

### 1.2 Then you can execute the "create_venv.sh"

This script will (only works in Linux):

1. create a virtual environment called "venv"
2. activate the venv
3. install the requirements in venv
4. start the api

### 1.2.5 Or you can do all of this manually

(Linux)

1. Create venv :

```sh
python3 -m venv [venv-name]
```

2. Open venv :

```sh 
. venv/bin/activate
```
3. Install requirements :

```sh
pip install -r requirements.txt
```

4. Open the api folder :

```sh 
cd api_seelect/
```

(Windows)

1. Create venv :

```sh 
virtualenv --python C:\Path\To\Python\python.exe venv
```

or

'''sh
python -m venv venv
'''

2. Open venv :

```sh 
./venv/Scripts/activate
```

3. Install requirements :

```sh
pip install -r requirements.txt
```

4. Open the api folder :

```sh 
cd api_seelect/
```

If you want to close the venv, just use the command :

(Windows and Linux)

```sh 
deactivate
```

### 1.3 Start API

You can start using the command (in this case the adresse ip will be localhost [127.0.0.1]) :

```sh 
python3 manage.py runserver
```

If you want to use a specific ip, just add after runserver :

```sh 
python3 manage.py runserver [ip]
```
