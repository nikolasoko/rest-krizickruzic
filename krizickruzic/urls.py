"""krizickruzic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users import views as user_views
from game import views as game_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', user_views.UserRegistration.as_view(), name='register'),
    path('game_list/', game_views.GameList.as_view(), name='game_list'),
    path('filter/', game_views.FilteredGameList.as_view(), name='filter'),
    path('create_game/',game_views.CreateGame.as_view(), name ='create_game'),
    path('join_game/', game_views.joinGame,name='join_game'),
    path('make_move/', game_views.MakeMove.as_view(),name ='make_move'),
    path('game_status/', game_views.GameStatus.as_view(),name ='game_status'),
    path('display_profile/',user_views.displayProfile,name ='disp'),

]
