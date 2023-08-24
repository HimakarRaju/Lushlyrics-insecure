


## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/mohammedwed/lushlyrics-webapp-django.git
$ cd lushlyrics-webapp-django
```

Create a virtual environment to install dependencies in and activate it:

```sh
python -m virtualenv env
```

Activate virtual environment
```sh
#powershell
./env/scripts/activate.ps1

#cmd Prompt
source env/bin/activate
```

Then install the dependencies:

```sh
pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
cd spotify-clone-django
python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
