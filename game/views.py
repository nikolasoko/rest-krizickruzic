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
from django.db.models import Q





#klasa zadužene za paginaciju
class CustomPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

#klasa za kreiranje nove igre
class CreateGame(generics.CreateAPIView):
    serializer_class = GameSerializer



#funkcija koja pridružuje igrača određenoj igri ovisno o primljenom id-u igre i mjenja status igre u "u tijeku"
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

#paginirani pregled svih igara počevši od najnovijih
class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all().order_by('-created')
    serializer_class = GameSerializer
    pagination_class = CustomPagination


#filtrira sve igre ovisno o igraču,vremenu nastanka i statusu igre
class FilteredGameList(generics.ListCreateAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):

        queryset = Game.objects.all()
        username = self.request.query_params.get('player', None)
        status = self.request.query_params.get('game_status')
        date = self.request.query_params.get('created')
        before_flag=self.request.query_params.get('before_flag')
        if username is not None:
            queryset = queryset.filter(Q(first_player__username=username) | Q(second_player__username=username))
        if status is not None:
            queryset = queryset.filter(game_status=status)
        if date is not None:
            if before_flag=='True':
                queryset = queryset.filter(created__lte=date)
            else:
                queryset = queryset.filter(created__gt=date)
        return queryset    
#klasa prima id igre a vraca sve poteze oba igrača koji su odigrani u toj igri
class GameStatus(generics.ListAPIView):
    serializer_class = MoveSerializer

    def get_queryset(self):
        queryset = Move.objects.all()
        id=self.request.query_params.get('id', None)
        queryset = queryset.filter(game_id__id=id)
        return queryset

#provjeravamo dosadašnje stanje ploče i vračamo true ukoliko je igra završila a false ako se igra nastavlja
def checkWin(game:Game):

    #lista lista koje sadrže koordinate poteza koji donose pobjedu
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
    
    #radimo listu poteza koje je prvi igrač dosada odigrao i provjeravamo postoji li kombinacija za pobjedu 
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
            game.save()
            return True
    #radimo listu poteza koje je drugi igrač dosada odigrao i provjeravamo postoji li kombinacija za pobjedu
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
            game.save()
            return True
    #provjera jesu li sva polja popunjena bez pobjednika
    totalMoves=len(firstList) + len(secondList)
    if (totalMoves==9):
        serializer = GameSerializer(game)
        game.game_status="finished"
        game.save()
        return True
    return False
    
    
    
#klasa zadužena za dodavanje poteza u bazu
class MakeMove(generics.CreateAPIView):
    serializer_class = MoveSerializer

    #POST metoda prima username korisnika koji radi potez i id igre za u kojoj se potez odigrava
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
        #u slučaju da je potez proša sve validacije spremamo ga u u bazu i proveravamo stanje igre nakon poteza
        if m.is_valid():
            m.save()
            gameOver=checkWin(game)
            if (gameOver):
                g = GameSerializer(game)
                game.save()
                if game.winner is None:
                    return Response("Igra je završila neriješeno")
                return Response("Igra je završena, pobjednik je " + game.winner.username)
            return Response(m.data, status=201)
        else :
            return Response("Potez nije valjan",status=404)

        
        

