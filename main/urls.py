from django.urls import path
from . import views
from .views import *

urlpatterns = [

    path(''                 , views.default,                name='default'),

    path('login/'           , views.login_auth,             name='login_auth'),
    path('search/'          , views.search,                 name='search_page'),
    path('playlist/'        , views.playlist,               name='your_playlists'),

    path('logout/'          , views.logout_auth,            name='logout_auth'),


    path('passwordreset/'   ,views.passwordreset,           name='passwordreset'),

    path('changepassword/'  ,views.changepassword,          name='changepassword'),

    path('signup/'          , views.signup,                 name='signup'),
]
