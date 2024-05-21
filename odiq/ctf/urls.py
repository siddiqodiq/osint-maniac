from django.urls import path
from .views import download_file
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('404', views.error, name='error'),
    path('register', views.signup, name='signup'),
    path('about', views.about, name='about'),
    path('login', views.login1, name='login1'),
    path('instructions', views.inst, name='inst'),
    path('quest', views.Quest, name='Quest'),
    path('logout', views.logout, name='logout'),
    path('check', views.check, name='check'),
    path('hint', views.hint, name='hint'),
    path('scoreboard', views.leaderboard, name='scoreboard'),
    path('profil', views.profil, name='profil'),
    path('download/<int:question_id>/', download_file, name='download_file'),
    path('quest/tools', views.tools, name='tools'),
    path('game', views.game, name='game' )
]
