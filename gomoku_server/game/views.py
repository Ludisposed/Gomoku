from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

import json
from game.util import (parse_request, user_login, user_regist, 
                       user_logout, online_users, invite_game,
                       invite_info, start_game, move)

@csrf_exempt
def Login(request):
    '''
    POST request parameter
    user:string
    password:string
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "user" not in content or "password" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:user/password is needed"}'))
        msg = user_login(content["user"], content["password"])
        if msg != "Success":
            return HttpResponse(json.dumps('{{"code":10010, "errmsg":\"{}\"}}'.format(msg)))

        return HttpResponse(json.dumps('{"code":10000, "content":"Login Success"}'))
    else:
        raise Http404


@csrf_exempt
def Regist(request):
    '''
    POST request parameter
    user:string
    password:string
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "user" not in content or "password" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:user/password is needed"}'))
        msg = user_regist(content["user"], content["password"])
        if msg != "Success":
            return HttpResponse(json.dumps('{{"code":10010, "errmsg":\"{}\"}}'.format(msg)))

        return HttpResponse(json.dumps('{"code":10000, "content":"Regist Success"}'))
    else:
        raise Http404

@csrf_exempt
def Logout(request):
    '''
    POST request parameter
    user:string
    password:string
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "user" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:user is needed"}'))
        msg = user_logout(content["user"])
        if msg != "Success":
            return HttpResponse(json.dumps('{{"code":10010, "errmsg":\"{}\"}}'.format(msg)))

        return HttpResponse(json.dumps('{"code":10000, "content":"Logout Success"}'))
    else:
        raise Http404


@csrf_exempt
def OnLine(request):
    if request.method == "POST":
        users = online_users()
        return HttpResponse(json.dumps('{{"code":10000, "content":{}}}'.format(users)))
    else:
        raise Http404

@csrf_exempt
def Invite(request):
    '''
    POST request parameter
    from:string
    to:string
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "from" not in content or "to" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:from/to is needed"}'))
        msg = invite_game(content["from"], content["to"])
        if msg != "Success":
            return HttpResponse(json.dumps('{{"code":10010, "errmsg":\"{}\"}}'.format(msg)))
        return HttpResponse(json.dumps('{"code":10000, "content":"Success"}'))
    else:
        raise Http404

@csrf_exempt
def Beinvited(request):
    '''
    POST request parameter
    from:string
    to:string
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "me" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:me is needed"}'))
        msg = invite_info(content["me"])
        if msg == "User not exist":
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"You gave me a fake user, no one invite fake user"}'))
        return HttpResponse(json.dumps('{{"code":10000, "content":{}}}'.format(msg)))
    else:
        raise Http404

@csrf_exempt
def StartGame(request):
    '''
    POST request parameter
    from:string
    to:string
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "player1" not in content or "player2" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:player1/player2 is needed"}'))
        msg = start_game(content["player1"], content["player2"])
        if msg != "Success":
            return HttpResponse(json.dumps('{{"code":10010, "errmsg":\"{}\"}}'.format(msg)))

        return HttpResponse(json.dumps('{"code":10000, "content":"Success"}'))
    else:
        raise Http404


@csrf_exempt
def Move(request):
    '''
    POST request parameter
    player:string
    cordinate_x:Int
    cordinate_y:Int
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "player" not in content or "cordinate_x" not in content or "cordinate_y" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:player/cordinate_x/cordinate_y is needed"}'))
        position = int(content["cordinate_x"]) * 15 + int(content["cordinate_y"])
        statue, msg = move(content["player"], position)
        if statue == 0:
            return HttpResponse(json.dumps('{{"code":10010, "errmsg":\"{}\"}}'.format(msg)))
        elif statue == 3:
            return HttpResponse(json.dumps('{{"code":10010, "content":\"{}\", "finish":False, "winner":-1}}'.format(msg)))
       
        return HttpResponse(json.dumps('{{"code":10010, "content":\"{}\", "finish":True, "winner":{}}}'.format(msg, statue)))
    else:
        raise Http404
    