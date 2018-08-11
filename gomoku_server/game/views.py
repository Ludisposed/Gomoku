from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

import json
from game.util import parse_request

@csrf_exempt
def Login(request):
    '''
    POST request parameter
    name:string
    password:string
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "name" not in content or "password" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:name/password is needed"}'))
        
        return HttpResponse(json.dumps(json_data))
    else:
        raise Http404


@csrf_exempt
def Regist(request):
    '''
    POST request parameter
    name:string
    password:string
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "name" not in content or "password" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:name/password is needed"}'))

        return HttpResponse(json.dumps(json_data))
    else:
        raise Http404

@csrf_exempt
def Move(request):
    '''
    POST request parameter
    player:Int
    cordinate_x:Int
    cordinate_y:Int
    '''
    if request.method == "POST":
        content = parse_request(request)
        if "player" not in content or "cordinate_x" not in content or "cordinate_y" not in content:
            return HttpResponse(json.dumps('{"code":10010, "errmsg":"[-] Error:player/cordinate_x/cordinate_y is needed"}'))

        return HttpResponse(json.dumps(json_data))
    else:
        raise Http404
    