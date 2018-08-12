# -*- coding: utf-8 -*-
'''
Game Process:
1. login/regist->login
2. check online users -> send invitation
3. check any invitation to me -> accept invitation
4. move piece
'''
import sys
from time import sleep
from helper import(login, regist, logout, invite, beInvited, 
                   startGame, onlineUser, currentgame, move)


class GomokuGame():
    def __init__(self):
        self.username=None
        self.password=None
        self.turn=None
    
    def login_game(self, username, password):
        state, msg = login(username, password)
        if state:
            self.username = username
            self.password = password
        return state, msg

    def regist_game(self, username, password):
        state, msg = regist(username, password)
        if state:
            self.username = username
            self.password = password
        return state, msg

    def online_user(self):
        state, msg = onlineUser()
        if state:
            msg = sorted([m for m in msg if m != self.username])
        return state, msg

    def send_invitation(self, touser):
        if self.username is None:
            return False, "Please Login first"
        return invite(self.username, touser)

    def receive_invitation(self):
        if self.username is not None:
            return beInvited(self.username, self.password)
        return False, None

    def start_game(self, withuser):
        if self.username is None:
            return False, "Please Login first"
        return startGame(self.username, withuser)

    def game_state(self):
        if self.username is None:
            return False, "Please Login first"
        state, msg = currentgame(self.username, self.password)
        if state:
            if self.turn is None or self.turn != msg["myturn"]:
                self.turn = msg["myturn"]
                board = "\n".join(["".join(["{:3}".format(msg["board"][i:i+15][j]) \
                                            for j in range(15)]) \
                                   for i in range(0,225,15)])

                return state, {"board":board, "turn":self.turn}
            else:
                return state, None
        return state, msg

    def add_piece(self, cordinate_x, cordinate_y):
        if self.username is None:
            return False, "Please Login first"
        return move(self.username, self.password, cordinate_x, cordinate_y)

def welcome():
    print("Welcome to Gomoku Game")
    while True:
        choice = input("Please choce 1) Login 2) Regist 3) quit: ")
        try:
            choice = int(choice)
            if choice not in [1,2,3]:
                continue
            return choice
        except:
            continue

def user_login(game, regist=False):
    process = "Login" if not regist else "Regist"
    username = input(f"{process} username: ")
    password = input(f"{process} password: ")
    if regist:
        state, msg = game.regist_game(username[:20], password[:20])
    else:
        state, msg = game.login_game(username[:20], password[:20])
    if state:
        print(f"Welcome {username}")
    else:
        print(f"Fail to {process} using {username}/{password} Error: {msg}")
    return state

def send_invitation(game, onlineusers):
    print("Online Users:\n")
    print("\n0) Keep waiting\n")
    print("\n".join([f"{i+1}) {u}" for i, u in enumerate(onlineusers)]))
    
    while True:
        choice = input("Sent invitation to user: ")
        try:
            choice = int(choice)
            if choice not in range(len(onlineusers)+1):
                continue
            if choice == 0:
                return 2
            state, msg = game.send_invitation(onlineusers[choice-1])
            if not state:
                print(msg)
            return state
        except:
            continue
    return False

def accept_invitation(game, invitation_users):
    print("Invitations from Users:\n")
    print("\n".join([f"{i+1}) {u}" for i, u in enumerate(invitation_users)]))
    while True:
        choice = input("Accept invitation to user: ")
        try:
            choice = int(choice)
            if choice not in range(1,len(invitation_users)+1):
                continue
            state, msg = game.start_game(invitation_users[choice-1])
            if not state:
                print(msg)
            return state
        except:
            continue
    return False

def invite_join_game(game):
    state, msg = game.online_user()
    if not state:
        print(f"Failed to fetch online user Error: {msg}")
    else:
        while True:
            if len(msg) == 0:
                print("No other user Online now, waiting others...")
                waiting = input("continue waiting? [y/n] ")
                if waiting != "y":
                    return False
                sleep(10)
            else:
                s = send_invitation(game, msg)
                if s != 2:
                    return s
                sleep(5)

            invited_state, invitors = game.receive_invitation()
            if invited_state:

                s = accept_invitation(game, invitors)
                print(s)
                if s:
                    return True

            state, msg = game.online_user()
    return state

def playing_game(game):
    pass


def main(game):
    choice = welcome()
    if choice == 3:
        sys.exit(0)

    
    if not user_login(game, (choice == 2)):
        sys.exit(1)

    state, msg = game.game_state()
    while not state:
        if not invite_join_game(game):
            sys.exit(1)
        state, msg = game.game_state()

    while state:
        if msg is not None:
            print(msg["board"])
            if msg["turn"]:
                while True:
                    position = input("Add piece in postion, [ex: 0,0]: ")
                    try:
                        x, y  = list(map(int, position.split(",")))
                        state, msg_game = game.add_piece(x,y)
                        print(state, msg_game)
                        if not state:
                            print(msg_game)
                            continue
                        if msg_game["finish"]:
                            print(f"\nGame finished: winner is {msg['winner']}")
                            sys.exit(0)
                        break
                    except:
                        continue
            else:
                print("Waiting...")

        state, msg = game.game_state()
        print(state, msg)


if __name__ == "__main__":
    game = GomokuGame()
    main(game)
    
    