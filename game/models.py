from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

#Game model zadužen za osnovne informacije o igri
class Game(models.Model):
    first_player = models.ForeignKey(User, related_name='first_player', on_delete=models.CASCADE)
    second_player = models.ForeignKey(User,related_name='second_player',blank=True, null=True, on_delete=models.CASCADE)
    game_status=models.CharField(max_length=30,blank=True, default="open")
    first_player_piece=models.CharField(max_length=1)
    created = models.DateTimeField(auto_now_add=True)
    winner = models.ForeignKey(User,related_name='winner',null=True,blank=True,on_delete=models.CASCADE)



#klasa koja sadrži infomarcije o svakom potezu: id igrača koji su igrali, id igre i koordinatepoteza na polju
class Move(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    board_row=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)],default=0,blank=True)
    board_column=models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)],default=0,blank=True)
    created = models.DateTimeField(auto_now_add=True)
