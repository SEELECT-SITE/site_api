# SEELECT API

## 0. Introduction

SEEELECT means "SEMANA DAS ENGENHARIAS DE COMPUTAÇÃO, ELÉTRICA E TELECOMUNICAÇÕES", which is the week reserved to promote the graduation courses of electrical, telecommunications and computer engineering. In SEELECT we have workshops, courses, speeches, visits to companies. To enjoy that, you should pay for a kit, which have some types:

- Free
- Discovery
- Explorer
- Premium

Each kit allows you to participate of a specific number of activities. The Free version, allows you to participate of the speeches proportioned by the sponsors of the SELECT, so on the opening and ending events.

So to manage the users, events, kits, authentication, permissions, and other stuffs, like contact messages on the website, I created this API using Django, to support the front-end. 

The project was made in 1–2 months by a student, me, so logically it has some problems and many features that were thought and not implemented, probably I'll implement until the next SELECT, in 2024.

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

```sh
python -m venv venv
```

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

[Linux]
```sh 
python3 manage.py runserver
```

[Windows]
```sh 
python manage.py runserver
```

If you want to use a specific ip, just add after runserver :

[Linux]
```sh 
python3 manage.py runserver [ip]
```

[Windows]
```sh 
python manage.py runserver [ip]
```
