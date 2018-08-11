from django.db import models

# Create your models here.

DEFAULT_USER_ID = DEFAULT_GAME_ID = DEFAULT_STEP_ID = 1
DEFAULT_PASSWORD="123456"
DEFAULT_BOARD="2"*225

class User(models.Model):
    name=models.CharField(max_length=20)
    password=models.CharField(max_length=32, default=DEFAULT_PASSWORD)
    online=models.BooleanField(default=False)
    gaming=models.BooleanField(default=False)

class Game(models.Model):
    player1=models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER_ID, related_name="fk_g_p1_id")
    player2=models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER_ID, related_name="fk_g_p2_id")
    board=models.CharField(max_length=255, default=DEFAULT_BOARD)
    finished=models.BooleanField(default=False)
    start_timestamp=models.DateField(auto_now=True)
    end_timestamp=models.DateField(auto_now=True)
    result=models.IntegerField(default=0)

class Step(models.Model):
    board=models.CharField(max_length=255)

class Record(models.Model):
    game=models.ForeignKey(Game, on_delete=models.CASCADE, default=DEFAULT_GAME_ID, related_name="fk_re_g_id")
    step=models.ForeignKey(Step, on_delete=models.CASCADE, default=DEFAULT_STEP_ID, related_name="fk_re_s_id")

class Result(models.Model):
    game=models.ForeignKey(Game, on_delete=models.CASCADE, default=DEFAULT_GAME_ID, related_name="fk_r_g_id")
    winner=models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER_ID, related_name="fk_r_w_id")
    loser=models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER_ID, related_name="fk_r_l_id")

class Invite(models.Model):
    fromuser=models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER_ID, related_name="fk_i_f_id")
    touser=models.ForeignKey(User, on_delete=models.CASCADE, default=DEFAULT_USER_ID, related_name="fk_i_t_id")
    invite_timestamp=models.DateField(auto_now=True)



