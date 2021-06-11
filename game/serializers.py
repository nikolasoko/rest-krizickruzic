from django.contrib.auth import models
from django.db.models import fields
from django.db.models.query import QuerySet
from rest_framework.fields import SlugField
from game.models import Game,Move
from django.db.models.fields import CharField
from rest_framework import serializers,relations
from django.contrib.auth.models import User

class GameSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    #first_player = serializers.CharField(source='first_player.username')
    #second_player = serializers.CharField(source='second_player.username',allow_null=True,allow_blank=True)
    first_player = serializers.SlugRelatedField(slug_field='username',many=False,
        read_only=False,queryset=models.User.objects.all())

    second_player = serializers.SlugRelatedField(slug_field='username',many=False,
        read_only=False,queryset=models.User.objects.all(),allow_null=True)

    game_status=serializers.CharField(max_length=30,default="open")
    first_player_piece=serializers.CharField(max_length=1)
    created = serializers.DateTimeField(read_only=True)
    winner = serializers.SlugRelatedField(slug_field='winner',many=False,
        read_only=False,queryset=models.User.objects.all(),allow_null=True)

    """def get_username(self, obj):
        return obj.first_player.username"""

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
        
"""    def create(self, validated_data):
        ime = validated_data.pop('first_player','')
        user = User.objects.filter(username=ime).first()
        #user = User.objects.get(username=ime)
        secondplayer = validated_data.pop('second_player', '')
        #user = queryset.filter(username=ime)
        validated_data['first_player']=user
        game = Game.objects.create(**validated_data)
        #game.first_player=user[0]
        #game.set_second_player("")
        game.save()
        return game"""


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
