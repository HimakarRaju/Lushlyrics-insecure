import json
from email import message
import uuid

from django.contrib import admin, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import include, path
from django.urls.base import reverse
from youtube_search import YoutubeSearch

from .helpers import send_forget_password_mail
from .models import *
from .models import playlist_user
from .views import *

# import cardupdate


f = open('card.json', 'r')
CONTAINER = json.load(f)


def default(request):
    global CONTAINER

    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html', {'CONTAINER': CONTAINER, 'song': song})


def playlist(request):  # type: ignore
    cur_user = playlist_user.objects.get(username=request.user)
    try:
        song = request.GET.get('song')
        song = cur_user.playlist_song_set.get(song_title=song)  # type: ignore
        song.delete()
    except:
        pass
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()  # type: ignore
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song': song, 'user_playlist': user_playlist})


def search(request):
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    try:
        search = request.GET.get('search')
        song = YoutubeSearch(search, max_results=10).to_dict()
        song_li = [song[:10:2], song[1:10:2]]
        # print(song_li)
    except:
        return redirect('/')

    return render(request, 'search.html', {'CONTAINER': song_li, 'song': song_li[0][0]['id']})


def add_playlist(request):
    cur_user = playlist_user.objects.get(username=request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):  # type: ignore

        songdic = (YoutubeSearch(
            request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc = songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'], song_dur=request.POST['duration'],  # type: ignore
                                          song_albumsrc=song__albumsrc,
                                          song_channel=request.POST['channel'], song_date_added=request.POST['date'], song_youtube_id=request.POST['songid'])


# adding logout code
def logout_auth(request):
    logout(request)
    return redirect('/login')

# adding playlist code


def playlist(request):
    if request.user.is_anonymous:
        return redirect('/login')
    cur_user = playlist_user.objects.get(username=request.user)
    try:
        song = request.GET.get('song')
        song = cur_user.playlist_song_set.get(song_title=song)  # type: ignore
        song.delete()
    except:
        pass
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()  # type: ignore
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song': song, 'user_playlist': user_playlist})


# =================================================================================================================#


def signup(request):
    context = {'username': True, 'email': True}
    if not request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if (username) in User.objects.values_list("username"):
            context['username'] = False
            return render(request, 'signup.html', context)
        elif (email) in User.objects.values_list("email"):
            context['email'] = False
            return render(request, 'signup.html', context)

        playlist_user.objects.create(username=username)
        new_user = User.objects.create_user(username, email, password)
        new_user.save()
        login(request, new_user)

        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()

        profile_obj = Profile.objects.create(user=user_obj)
        profile_obj.save()
        return redirect('/')

    return render(request, 'signup.html', context)


def login_auth(request):

    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                messages.success(
                    request, 'Both Username and Password are required.')
                return redirect('/login/')
            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.success(request, 'User not found.')
                return redirect('/login/')

            user = authenticate(username=username, password=password)

            if user is None:
                messages.success(request, 'Wrong password.')
                return redirect('/login/')

            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            profile_obj = Profile.objects.create(user=user_obj)
            profile_obj.save()
            return redirect('/')

            login(request, user)
            return redirect('/')

    except Exception as e:
        print(e)
    return render(request, 'login.html')


def passwordreset(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'user not found with this username.')
                return redirect('/password_reset_form/')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('/password_reset_form/')

    except Exception as e:
        print(e)
    return render(request, 'password_reset_form.html')


def password_reset_form(request):
    return render(request, 'password_reset_form.html')


def changepassword(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(
            forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')

    except Exception as e:
        print(e)
    return render(request, 'change-password.html', context)
