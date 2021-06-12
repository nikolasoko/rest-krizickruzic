from django.contrib.auth import models
from django.db.models import fields
from django.db.models.query import QuerySet
from rest_framework.fields import SlugField
from game.models import Game,Move
from django.db.models.fields import CharField
from rest_framework import serializers,relations
from django.contrib.auth.models import User

#serializer za model Game
class GameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_player = serializers.SlugRelatedField(slug_field='username',many=False,
        read_only=False,queryset=models.User.objects.all())

    second_player = serializers.SlugRelatedField(slug_field='username',many=False,
        read_only=False,queryset=models.User.objects.all(),allow_null=True)

    game_status=serializers.CharField(max_length=30,default="open")
    first_player_piece=serializers.CharField(max_length=1)
    created = serializers.DateTimeField(read_only=True)
    winner = serializers.SlugRelatedField(slug_field='username',many=False,
        read_only=False,queryset=models.User.objects.all(),allow_null=True)


    class Meta:
        model = Game
        fields= (
            'id',
            'first_player',
            'second_player',
            'game_status',
            'first_player_piece',
            'created',
            'winner',
        )
        read_only_fields = ('id','created')
        

#serializer za model Move
class MoveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    game_id = serializers.SlugRelatedField(slug_field='id',many=False,
        read_only=False,queryset=Game.objects.all())
    player = serializers.SlugRelatedField(slug_field='username',many=False,
        read_only=False,queryset=models.User.objects.all())
    #game_id=serializers.IntegerField(source='game.id')
    board_row=serializers.IntegerField(min_value=0, max_value=2)
    board_column=serializers.IntegerField(min_value=0, max_value=2)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Move
        fields= (
            'id',
            'player',
            'game_id',
            'board_row',
            'board_column',
            'created',
        )
        read_only_fields = ('id','created')
