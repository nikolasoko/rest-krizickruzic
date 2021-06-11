from django.db.models import Q
from game.models import Game
from django.contrib.auth.models import User
from rest_framework.views import APIView
from users.serializers import UserSerializer
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
#ovo vidjeti
from django.views.decorators.csrf import csrf_exempt


# Create your views here.




class UserRegistration(generics.CreateAPIView):
    serializer_class = UserSerializer



@api_view(['GET'])
def displayProfile(request):
    queryset = Game.objects.all()
    username=request.query_params.get('username', None)
    games = queryset.filter(Q(first_player__username=username) | Q(second_player__username=username))
    numberOfGames=games.count()
    wins = queryset.filter(winner__username=username).count()
    winpercent=0
    if numberOfGames!=0:
        winpercent=(wins/numberOfGames)*100
    dict={'username':username, 'numberOfGames':numberOfGames,'win percent':winpercent}
    return JsonResponse(dict)