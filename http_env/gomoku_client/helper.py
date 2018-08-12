# -*- coding: utf-8 -*-
import urllib.parse
import json
import requests

URL="http://127.0.0.1:8000"

def _post( path, data):
    try:
        response = requests.post(urllib.parse.urljoin(URL, path), data=data)
        if response.status_code in [408, 504]:
            return False, None
        elif response.status_code != 200:
            return False, f"Error: {response.status_code}"
        server_response = json.loads(response.text)
        if server_response["code"] != 10000:
            return False, server_response["errmsg"]
        return True, server_response["content"]
    except Exception as e:
        return False, str(e)

def _post_return( path, data, process_name):
    recall = 0
    status, msg = _post( path, data)
    while True:
        if not status and msg is None:
            if recall < 6:
                status, msg = _post(path, data)
                recall += 1
            else:
                return False, f"failed to {process_name}, try later"
        elif not status:
            return False, msg
        else:
            return True, msg

def login( username, password):
    data = {"user":username, "password":password}
    return _post_return( "user/login", data, "login")

def regist( username, password):
    data = {"user":username, "password":password}
    return _post_return( "user/regist", data, "regist")

def logout( username, password):
    data = {"user":username, "password":password}
    return _post_return( "user/logout", data, "logout")

def invite( from_username, to_username):
    data = {"from":from_username, "to":to_username}
    return _post_return( "user/invite", data, "invite")

def beInvited( username, password):
    data = {"user":username, "password":password}
    return _post_return( "user/invited", data, "invite")

def startGame( player1, player2):
    data = {"player1":player1, "player2":player2}
    return _post_return( "user/startgame", data, f"{player1}/{player2} start game")

def onlineUser():
    return _post_return( "user/online", None, "online user")

def currentgame( username, password):
    data = {"user":username, "password":password}
    return _post_return( "user/currentgame", data, "currentgame")

def move( username, password, cordinate_x, cordinate_y):
    data = {"user":username, "password":password, "cordinate_x":cordinate_x, "cordinate_y":cordinate_y}
    return _post_return( "user/move", data, "online user")

