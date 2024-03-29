from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'signUps'

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^editProfile/$',views.editProfile,name='editProfile'),
    url(r'^createGame/$',views.createGame,name='createGame'),
    url(r'^myGames/$',views.displayMyGames,name='myGames'),
    path('games/<int:game_id>/', views.gamebyId, name='gamebyID'),
    path('user/<int:profile_id>/', views.profilebyID, name='profilebyID'),
    url(r'^allGames/$',views.displayAllGames,name='allGames'),
    url(r'^attend_game', views.attendGame, name='attendGame'),
    url(r'^leave_game/', views.leaveGame, name='leaveGame'),
    url(r'^delete_game/', views.deleteGame, name='deleteGame'),
    url(r'^center_map/', views.centerMap, name='centerMap'),
    url(r'^add_teammate', views.addTeammate, name='addTeammate'),
    url(r'^remove_teammate/', views.removeTeammate, name='removeTeammate'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)