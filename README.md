
# Setup

The first thing to do is to clone the repository:

```sh
git clone https://github.com/mohammedwed/lushlyrics-webapp-django.git
cd lushlyrics-webapp-django
```

Create a virtual environment to install dependencies in and activate it:

```sh
python -m virtualenv env
```

Activate virtual environment

```sh
#powershell
./env/scripts/activate.ps1
```

```sh
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
python manage.py runserver
```

And navigate to `http://127.0.0.1:8000/`.

***THE FINAL RESULTS AFTER ADDING THE LOGIN, REGISTER, FORGOT PASSWORD AND CHANGE PASSWORD***

***The main screen after login***
![image](../Lushlyrics-insecure/IMAGES/(1).png)

***Login Screen***
![image](../Lushlyrics-insecure/IMAGES/(2).png)

***Password Reset Screen***
![image](../Lushlyrics-insecure/IMAGES/(3).png)

***Sign Up Screen***
![image](../Lushlyrics-insecure/IMAGES/(4).png)

Password Mail sent Screen***
![image](../Lushlyrics-insecure/IMAGES/(5).png)

***New Password Screen***
![image](../Lushlyrics-insecure/IMAGES/(8).png)

***Password Changed Success Screen***
![image](../Lushlyrics-insecure/IMAGES/(9).png)
