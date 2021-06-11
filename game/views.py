from django.db.models.query import QuerySet
from rest_framework import pagination
from game.models import Game, Move
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from game.serializers import GameSerializer, MoveSerializer
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status



GAMESTATUS={'o':'open','progress':'','f':'finished'}


class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

class CreateGame(generics.CreateAPIView):
    serializer_class = GameSerializer




@api_view(['PATCH',])
def joinGame(request):
    id = request.POST.get('id', False)
    second_player = request.POST.get('second_player', False)
    queryset = User.objects.all()
    queryset = queryset.filter(username=second_player).first()
    game=get_object_or_404(Game,id=id)
    game.second_player=queryset
    game.game_status='progress'
    game.save()
    serializer = GameSerializer(game)
    return Response(serializer.data)


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all().order_by('-created')
    serializer_class = GameSerializer
    pagination_class = CustomPagination
    
class FilteredGameList(generics.ListCreateAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):

        queryset = Game.objects.all()
        username = self.request.query_params.get('first_player', None)
        status = self.request.query_params.get('game_status')
        date = self.request.query_params.get('created')
        before_flag=self.request.query_params.get('before_flag')
        if username is not None:
            queryset = queryset.filter(first_player__username=username)
        if status is not None:
            queryset = queryset.filter(game_status=status)
        if date is not None:
            if before_flag=='True':
                queryset = queryset.filter(created__lte=date)
            else:
                queryset = queryset.filter(created__gt=date)
        return queryset    

class GameStatus(generics.ListAPIView):
    serializer_class = MoveSerializer

    def get_queryset(self):
        queryset = Move.objects.all()
        id=self.request.query_params.get('id', None)
        queryset = queryset.filter(game_id__id=id)
        return queryset

def checkWin(game:Game):
    WIN=[[(0,0),(0,1),(0,2)],
        [(1,0),(1,1),(1,2)],
        [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)],
        [(0,1),(1,1),(2,1)],
        [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)],
        [(2,0),(1,1),(0,2)]]

    queryset = Move.objects.all()
    queryset = queryset.filter(game_id__id=game.id)
    firstPlayermMoves=queryset.filter(player=game.first_player)
    secondPlayerMoves=queryset.filter(player=game.second_player) 
    
    
    firstList=[]
    for move in firstPlayermMoves:
        x=move.board_column
        y=move.board_row
        firstList.append((x,y))

    for x in WIN:
        check =  all(item in firstList for item in x)
        if check:
            serializer = GameSerializer(game)
            game.winner=game.first_player
            game.game_status="finished"
            game.save
            return True

    secondList=[]
    for move in secondPlayerMoves:
        x=move.board_column
        y=move.board_row
        secondList.append((x,y))

    for x in WIN:
        check =  all(item in secondList for item in x)
        if check:
            serializer = GameSerializer(game)
            game.winner=game.second_player
            game.game_status="finished"
            game.save
            return True

    totalMoves=len(firstList) + len(secondList)
    if (totalMoves==9):
        serializer = GameSerializer(game)
        game.game_status="finished"
        game.save
    return False
    
    
    

class MakeMove(generics.CreateAPIView):
    serializer_class = MoveSerializer

    def post(self,request):
        queryset = Move.objects.all()
        id=request.data['game_id']
        player=request.data['player']
        queryset = queryset.filter(game_id__id=id)
        game=Game.objects.filter(id=id).first()
        if (game.first_player.username != player and game.second_player.username !=player):
            return Response(
                    {
                        'message' : 'Odabrani igrač ne pripada igri !'
                    },status=409
                )
        
        for move in queryset:
            if move.board_column==int(request.data['board_column']) and move.board_row== int(request.data['board_row']):
                return Response(
                    {
                        'message' : 'Polje nije prazno !'
                    },status=409
                )
        m = MoveSerializer(data=request.data)
        if m.is_valid():
            m.save()
            gameOver=checkWin(game)
            if (gameOver):
                g = GameSerializer(game)
                g.save
                if game.winner.username=="":
                    return Response("Igra je završila neriješeno")
                return Response("Igra je završena, pobjednik je " + game.winner.username)
            return Response(m.data, status=201)
        else :
            return Response("Potez nije valjan",status=404)

        
        

