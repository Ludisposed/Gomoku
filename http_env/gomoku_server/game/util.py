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

def user_logout(username, password):
    try:
        user = User.objects.get(name=username)
        if password != user.password:
            return "Wrong Password"
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
        Invite.objects.create(fromuser=fromuser, touser=touser)
        return "Success"
    except ObjectDoesNotExist:
        return "From/to user not exist"

def invite_info(username, password):
    try:
        start_time = datetime.now() - timedelta(minutes=5)
        end_time = datetime.now()
        user = User.objects.get(name=username)
        if password != user.password:
            return "Wrong Password"
        invited = Invite.objects.filter(touser=user.id, invite_timestamp__range=(start_time, end_time))
        return [User.objects.get(id=i.fromuser.id).name for i in invited if valid_user(i.fromuser.id)]
    except ObjectDoesNotExist:
        return "User not exist"

def start_game(player1_name, player2_name):
    try:
        player1 = User.objects.get(name=player1_name)
        player2 = User.objects.get(name=player2_name)
        if player1.gaming or player2.gaming:
            return f"{player1_name}/{player2_name} is in Game"

        start_time = datetime.now() - timedelta(minutes=5)
        end_time = datetime.now()
        invite = Invite.objects.filter(fromuser=player1.id, touser=player2.id, invite_timestamp__range=(start_time, end_time))
        
        if len(invite) == 0:
            return f"No invitation infomation from {player1_name} to {player2_name}"

        User.objects.filter(name=player1.name).update(gaming=True)
        User.objects.filter(name=player2.name).update(gaming=True)
        Game.objects.create(player1=player1, player2=player2, current_player=player1)

        return "Success"
    except ObjectDoesNotExist:
        return "Player1/Player2 not exist"

def current_game(username, password):
    try:
        user = User.objects.get(name=username)
        if password != user.password:
            return 0, "Wrong Password"
        if not user.gaming:
            return 0, "User is not in any game"
        game = Game.objects.filter(current_player=user.id)
        if len(game)>0:
            return 1, game[0].board
        game = Game.objects.filter(next_player=user.id)
        if len(game)>0:
            return 2, game[0].board
        User.objects.filter(id=user.id).update(gaming=False)
        return 0, "User is not in any game"
    except ObjectDoesNotExist:
        return 0, "User not exist"

def move(username, password, position):
    try:
        user = User.objects.get(name=username)
        if password != user.password:
            return 0, "Wrong Password"
        if not user.gaming:
            return 0, "User is not in any game"
        game,piece,another_player = game_user_in(user.id)
        if game is None:
            return 0, "User is not in any game"
        if game.current_player != user.id:
            return 0, "Not your turn"
        if game.board[position] != "2":
            return 0, "Invalid move"
        board = game.board[:position] + piece + game.board[position+1:]
        Game.objects.filter(id=game.id).update(board=board, current_player=game.next_player, next_player=game.current_player)
        step = Step.objects.create(board=board)
        Record.objects.create(game=game, step=step)
        game_status = game_finish(board, current_piece, [position // 15, position % 15])
        if game_status >= 0:
            Game.objects.filter(id=game.id).update(finished=True, result=game_status, end_timestamp=datetime.now())
            User.objects.filter(name=username).update(gaming=False)
            User.objects.filter(name=another_player).update(gaming=False)
            return game_status, board
        return 3, board
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
        return game_player1[0], 0, game_player1[0].player2

    game_player2 = Game.objects.filter(player2=userid, finished=False)
    if len(game_player2) > 0:
        return game_player2[0], 1, game_player2[0].player1
    return None, -1, -1

def game_finish(board, current_piece, position):
    if "2" not in board:
        return 2
    board = [board[i:i+15] for i in range(0,225,15)]
    directions = [([0, 1], [0, -1]), ([1, 0], [-1, 0]), ([-1, 1], [1, -1]), ([1, 1], [-1, -1])]
    for direction in directions:
        continue_chess = 0
        for i in range(2):
            p = position[:]
            while 0 <= p[0] < 15 and 0 <= p[1] < 15:
                if board[p[0]][p[1]] == current_piece:
                    continue_chess += 1
                else:
                    break
                p[0] += direction[i][0]
                p[1] += direction[i][1]
        if continue_chess >= 6:
            return current_piece

    return -1
        



