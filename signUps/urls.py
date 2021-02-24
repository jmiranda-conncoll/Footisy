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
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)