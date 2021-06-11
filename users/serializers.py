from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from game.models import Game
 

class UserSerializer(serializers.ModelSerializer):
    #password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

