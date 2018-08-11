# -*- coding: utf-8 -*-
from urllib.parse import parse_qsl
from game.models import User, Invite, Game, Step
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta

def parse_request(request):
    return dict(parse_qsl(request.body.decode("utf-8")))

def user_login(username, password):
    try:
        user = User.objects.get(name=username)
        if password != user.password:
            return "Wrong Password"
        User.objects.filter(name=username).update(online=True)
        return "Success"
    except ObjectDoesNotExist:
        return "User not Exist"

def user_regist(username, password):
    try:
        user = User.objects.get(name=username)
        return "User exists"
    except ObjectDoesNotExist:
        User.objects.create(name=username,
                            password=password)
        return "Success"

def user_logout(username):
    try:
        user = User.objects.get(name=username)
        User.objects.filter(name=username).update(online=False)
        return "Success"
    except ObjectDoesNotExist:
        return "User not exist"

def online_users():
    users = User.objects.filter(online=True, gaming=False)
    return [user.name for user in users]

def invite_game(from_username, to_username):
    try:
        fromuser = User.objects.get(name=from_username)
        touser = User.objects.get(name=to_username)
        if not valid_user(fromuser.id):
            return f"{fromuser.name} not ready for new game"
        if not valid_user(touser.id):
            return f"{touser.name} not ready for new game"
        Invite.objects.create(fromuser=fromuser.id, touser=touser.id)
        return "Success"
    except ObjectDoesNotExist:
        return "From/to user not exist"

def invite_info(username):
    try:
        start_time = datetime.now() - timedelta(minutes=5)
        end_time = datetime.now()
        user = User.objects.get(name=username)
        invited = Invite.objects.filter(touser=user.id, invite_timestamp__range=(start_time, end_time))
        return [User.objects.get(id=i.fromuser).name for i in invited if valid_user(i.fromuser)]
    except ObjectDoesNotExist:
        return "User not exist"

def start_game(player1_name, player2_name):
    try:
        player1 = User.objects.get(name=player1_name)
        player2 = User.objects.get(name=player2_name)
        User.objects.filter(name=player1).update(gaming=True)
        User.objects.filter(name=player2).update(gaming=True)
        Game.objects.create(player1=player1.id, player2=player2.id)

        return "Success"
    except ObjectDoesNotExist:
        return "Player1/Player2 not exist"

def move(username, position):
    try:
        user = User.objects.get(name=username)
        if not user.gaming:
            return 0, "User is not in any game"
        game,piece,another_player = game_user_in(user.id)
        if game is None:
            return 0, "User is not in any game"
        if game.board[position] != "2":
            return 0, "Invalid move"
        board = game.board[:position] + piece + game.board[position+1:]
        Game.objects.filter(id=game.id).update(board=board)
        step = Step.objects.create(board=board)
        Record.objects.create(game=game.id, step=step.id)
        game_status = game_finish(board)
        if game_status >= 0:
            Game.objects.filter(id=game.id).update(finished=True, result=game_status, end_timestamp=datetime.now())
            User.objects.filter(name=username).update(gaming=False)
            User.objects.filter(name=another_player).update(gaming=False)
            return 2, board
        return 1, board
    except ObjectDoesNotExist:
        return 0, "User not exist"

def valid_user(userid):
    try:
        user = User.objects.get(id=userid)
        if user.online and not user.gaming:
            return True
        return False
    except ObjectDoesNotExist:
        return False

def game_user_in(userid):
    game_player1 = Game.objects.filter(player1=userid, finished=False)
    if len(game_player1) > 0:
        return game_player1, 0, game_player2.player2

    game_player2 = Game.objects.filter(player2=userid, finished=False)
    if len(game_player2) > 0:
        return game_player2, 1, game_player2.player1
    return None, -1, -1

def game_finish(board):
    pass



