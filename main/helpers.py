import json
import uuid
from email import message

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import include, path
from django.urls.base import reverse
from youtube_search import YoutubeSearch
from .models import *
from .models import playlist_user
from .views import *

# def send_forget_password_mail(email , token ):
#     subject = 'Your forget password link'
#     message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message, email_from, recipient_list)
#     return True


def send_forget_password_mail(email, token):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'user not found with this username.')
                return redirect('/passwordreset/')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/changepassword/')

    except Exception as e:
        print(e)
